param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,

    [string]$EventDate = '2026-07-23',
    [string]$EventTime = '10:00',
    [int]$DurationMinutes = 45,
    [string]$Timezone = 'Asia/Jerusalem',
    [int]$CalendlyConnectionId = 6487860
)

$ErrorActionPreference = 'Stop'

if ($EventDate -notmatch '^\d{4}-\d{2}-\d{2}$') {
    throw 'EventDate must use YYYY-MM-DD.'
}

if ($EventTime -notmatch '^\d{2}:\d{2}$') {
    throw 'EventTime must use HH:mm.'
}

if ($DurationMinutes -le 0) {
    throw 'DurationMinutes must be positive.'
}

$null = [datetime]::ParseExact(
    "$EventDate $EventTime",
    'yyyy-MM-dd HH:mm',
    [Globalization.CultureInfo]::InvariantCulture
)

$eventRequest = [ordered]@{
    name = 'הדרכת מערכת PLAN-T'
    host = 'https://api.calendly.com/users/78b3470f-21e6-4400-9a1a-19291111e1f1'
    duration = $DurationMinutes
    date_setting = [ordered]@{
        type = 'date_range'
        start_date = $EventDate
        end_date = $EventDate
    }
    timezone = $Timezone
    location = [ordered]@{
        kind = 'zoom_conference'
    }
}

$moduleMetadata = [ordered]@{
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
            method = [ordered]@{ mode = 'chose'; label = 'POST' }
            headers = [ordered]@{ mode = 'chose'; items = @( $null ) }
        }
        parameters = [ordered]@{
            __IMTCONN__ = [ordered]@{
                data = [ordered]@{ scoped = 'true'; connection = 'calendly2' }
                label = 'sales'
            }
        }
    }
    designer = [ordered]@{ x = 0; y = 0; name = 'Create Calendly one-off event type' }
    parameters = @(
        [ordered]@{
            name = '__IMTCONN__'
            type = 'account:calendly2'
            label = 'Connection'
            required = $true
        }
    )
}

$blueprint = [ordered]@{
    name = "Create Calendly one-off $EventDate $EventTime"
    flow = @(
        [ordered]@{
            id = 1
            module = 'calendly:makeApiCall'
            version = 2
            parameters = [ordered]@{ __IMTCONN__ = $CalendlyConnectionId }
            mapper = [ordered]@{
                url = '/one_off_event_types'
                method = 'POST'
                headers = @(
                    [ordered]@{ key = 'Content-Type'; value = 'application/json' }
                )
                qs = @()
                body = ($eventRequest | ConvertTo-Json -Depth 10 -Compress)
            }
            metadata = $moduleMetadata
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

$scenarioRequest = [ordered]@{
    blueprint = ($blueprint | ConvertTo-Json -Depth 30 -Compress)
    teamId = 1621766
    scheduling = '{"type":"on-demand"}'
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$utf8NoBom = [Text.UTF8Encoding]::new($false)

[IO.File]::WriteAllText(
    (Join-Path $OutputDirectory 'one-off-blueprint.json'),
    ($blueprint | ConvertTo-Json -Depth 30 -Compress),
    $utf8NoBom
)

[IO.File]::WriteAllText(
    (Join-Path $OutputDirectory 'create-scenario-request.json'),
    ($scenarioRequest | ConvertTo-Json -Depth 35 -Compress),
    $utf8NoBom
)

[ordered]@{
    eventDate = $EventDate
    eventTime = $EventTime
    durationMinutes = $DurationMinutes
    timezone = $Timezone
    outputDirectory = (Resolve-Path $OutputDirectory).Path
} | ConvertTo-Json -Compress
