param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,

    [string]$ExpectedEventName = 'הדרכת מערכת PLAN-T',
    [string]$CalendlyUserUri = 'https://api.calendly.com/users/78b3470f-21e6-4400-9a1a-19291111e1f1',
    [int]$CalendlyConnectionId = 6487860,
    [int]$MondayConnectionId = 9828370,
    [string]$MondayBoardId = '5099813594',
    [string]$MondayConfigItemId = '3076389232',
    [string]$MondayLinkColumnId = 'text_mm578mx0'
)

$ErrorActionPreference = 'Stop'

$calendlyMetadata = [ordered]@{
    expect = @(
        [ordered]@{ name = 'url'; type = 'text'; label = 'URL'; required = $true },
        [ordered]@{ name = 'method'; type = 'select'; label = 'Method'; required = $true },
        [ordered]@{
            name = 'headers'
            type = 'array'
            label = 'Headers'
            spec = @(
                [ordered]@{ name = 'key'; type = 'text'; label = 'Key' },
                [ordered]@{ name = 'value'; type = 'text'; label = 'Value' }
            )
        },
        [ordered]@{
            name = 'qs'
            type = 'array'
            label = 'Query String'
            spec = @(
                [ordered]@{ name = 'key'; type = 'text'; label = 'Key' },
                [ordered]@{ name = 'value'; type = 'text'; label = 'Value' }
            )
        },
        [ordered]@{ name = 'body'; type = 'text'; label = 'Body' }
    )
    restore = [ordered]@{
        expect = [ordered]@{
            qs = [ordered]@{ mode = 'chose' }
            method = [ordered]@{ mode = 'chose'; label = 'GET' }
            headers = [ordered]@{ mode = 'chose'; items = @( $null ) }
        }
        parameters = [ordered]@{
            __IMTCONN__ = [ordered]@{
                data = [ordered]@{ scoped = 'true'; connection = 'calendly2' }
                label = 'sales'
            }
        }
    }
    designer = [ordered]@{ x = 0; y = 0; name = 'Read latest Calendly event type' }
    parameters = @(
        [ordered]@{
            name = '__IMTCONN__'
            type = 'account:calendly2'
            label = 'Connection'
            required = $true
        }
    )
}

$mondayMetadata = [ordered]@{
    expect = @(
        [ordered]@{ name = 'boardId'; type = 'select'; label = 'Board ID'; required = $true },
        [ordered]@{ name = 'create_labels_if_missing'; type = 'boolean'; label = 'Create Labels if Missing'; required = $true },
        [ordered]@{ name = 'itemId'; type = 'any'; label = 'Item ID'; required = $true },
        [ordered]@{
            name = 'columnValuesToChange'
            type = 'array'
            label = 'Column Values to Change'
            required = $true
            spec = @(
                [ordered]@{
                    name = 'columnId'
                    type = 'select'
                    label = 'Column ID'
                    dynamic = $true
                    options = [ordered]@{ store = @() }
                    required = $true
                    validate = $false
                }
            )
        }
    )
    restore = [ordered]@{
        expect = [ordered]@{
            boardId = [ordered]@{ mode = 'edit'; label = 'הרשמות להדרכות :: public' }
            columnValuesToChange = [ordered]@{
                mode = 'chose'
                items = @(
                    [ordered]@{ columnId = [ordered]@{ mode = 'chose'; label = 'קישור Calendly פעיל' } }
                )
            }
        }
        parameters = [ordered]@{
            __IMTCONN__ = [ordered]@{
                data = [ordered]@{ scoped = 'true'; connection = 'monday' }
                label = 'nataliconectionmonday (plan-t-company - natali koifman)'
            }
        }
    }
    designer = [ordered]@{ x = 300; y = 0; name = 'Publish Calendly link to Monday config' }
    parameters = @(
        [ordered]@{
            name = '__IMTCONN__'
            type = 'account:monday'
            label = 'Connection'
            required = $true
        }
    )
}

$blueprint = [ordered]@{
    name = 'Publish latest PLAN-T Calendly one-off link to Monday'
    flow = @(
        [ordered]@{
            id = 1
            module = 'calendly:makeApiCall'
            version = 2
            parameters = [ordered]@{ __IMTCONN__ = $CalendlyConnectionId }
            mapper = [ordered]@{
                url = '/event_types'
                method = 'GET'
                headers = @(
                    [ordered]@{ key = 'Content-Type'; value = 'application/json' }
                )
                qs = @(
                    [ordered]@{ key = 'user'; value = $CalendlyUserUri },
                    [ordered]@{ key = 'active'; value = 'true' },
                    [ordered]@{ key = 'sort'; value = 'created_at:desc' },
                    [ordered]@{ key = 'count'; value = '100' }
                )
                body = ''
            }
            metadata = $calendlyMetadata
        },
        [ordered]@{
            id = 2
            module = 'monday:ChangeMultipleColumnValues'
            version = 1
            parameters = [ordered]@{ __IMTCONN__ = $MondayConnectionId }
            filter = [ordered]@{
                name = 'Only the newly created PLAN-T one-off event'
                conditions = @(
                    @(
                        [ordered]@{
                            a = '{{1.collection[1].name}}'
                            b = $ExpectedEventName
                            o = 'text:equal'
                        }
                    )
                )
            }
            mapper = [ordered]@{
                itemId = $MondayConfigItemId
                boardId = $MondayBoardId
                columnValuesToChange = @(
                    [ordered]@{
                        columnId = $MondayLinkColumnId
                        columnValue = '{{1.collection[1].scheduling_url}}'
                    }
                )
                create_labels_if_missing = $false
            }
            metadata = $mondayMetadata
        }
    )
    metadata = [ordered]@{
        instant = $false
        version = 1
        designer = [ordered]@{ orphans = @() }
        scenario = [ordered]@{
            dlq = $false
            dataloss = $false
            maxErrors = 1
            autoCommit = $true
            roundtrips = 1
            sequential = $true
            confidential = $false
            freshVariables = $false
            autoCommitTriggerLast = $true
        }
    }
}

$patchRequest = [ordered]@{
    blueprint = ($blueprint | ConvertTo-Json -Depth 35 -Compress)
    name = $blueprint.name
    scheduling = '{"type":"on-demand"}'
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$utf8NoBom = [Text.UTF8Encoding]::new($false)

[IO.File]::WriteAllText(
    (Join-Path $OutputDirectory 'publish-link-blueprint.json'),
    ($blueprint | ConvertTo-Json -Depth 35 -Compress),
    $utf8NoBom
)

[IO.File]::WriteAllText(
    (Join-Path $OutputDirectory 'publish-link-patch-request.json'),
    ($patchRequest | ConvertTo-Json -Depth 40 -Compress),
    $utf8NoBom
)

[ordered]@{
    expectedEventName = $ExpectedEventName
    mondayConfigItemId = $MondayConfigItemId
    mondayLinkColumnId = $MondayLinkColumnId
    outputDirectory = (Resolve-Path $OutputDirectory).Path
} | ConvertTo-Json -Compress
