param(
    [Parameter(Mandatory = $true)]
    [string]$SourceBlueprint,

    [Parameter(Mandatory = $true)]
    [string]$OutputBlueprint
)

$ErrorActionPreference = 'Stop'

$sourceDocument = Get-Content -Raw -Encoding UTF8 $SourceBlueprint | ConvertFrom-Json
$blueprint = $sourceDocument.response.blueprint

function Copy-Module {
    param([int]$Id)

    $module = $blueprint.flow | Where-Object { $_.id -eq $Id }
    if (-not $module) {
        throw "Module $Id was not found in the source blueprint."
    }

    return $module | ConvertTo-Json -Depth 100 | ConvertFrom-Json
}

function New-MondayGetItemModule {
    param(
        [int]$Id,
        [string]$ItemId,
        [int]$X,
        [string]$Name
    )

    return [ordered]@{
        id = $Id
        mapper = [ordered]@{
            id = $ItemId
            boardId = '5099813594'
            showSubitems = $true
            showParentItem = $true
            disableOutputInterfaceCaching = $true
        }
        module = 'monday:GetItem'
        version = 1
        metadata = [ordered]@{
            designer = [ordered]@{ x = $X; y = 0; name = $Name }
            interface = @(
                [ordered]@{ name = 'id'; type = 'uinteger'; label = 'ID' },
                [ordered]@{ name = 'name'; type = 'text'; label = 'Name' },
                [ordered]@{
                    name = 'column_values'
                    type = 'array'
                    label = 'Column values'
                    spec = [ordered]@{
                        type = 'collection'
                        spec = @(
                            [ordered]@{ name = 'id'; type = 'text'; label = 'ID' },
                            [ordered]@{ name = 'title'; type = 'text'; label = 'Title' },
                            [ordered]@{ name = 'value'; type = 'any'; label = 'Value' },
                            [ordered]@{ name = 'text'; type = 'text'; label = 'Text' }
                        )
                    }
                },
                [ordered]@{
                    name = 'mappable_column_values'
                    type = 'collection'
                    label = 'Mappable column values'
                    spec = @(
                        [ordered]@{ name = 'name'; type = 'text'; label = 'Name' },
                        [ordered]@{ name = 'text_mm578mx0'; type = 'text'; label = 'קישור Calendly פעיל' },
                        [ordered]@{
                            name = 'email_mm50jkhy'
                            type = 'collection'
                            label = 'מייל'
                            spec = @(
                                [ordered]@{ name = 'email'; type = 'email'; label = 'Email' },
                                [ordered]@{ name = 'text'; type = 'text'; label = 'Text' },
                                [ordered]@{ name = 'value'; type = 'any'; label = 'Value' }
                            )
                        }
                    )
                }
            )
            restore = [ordered]@{
                expect = [ordered]@{ boardId = [ordered]@{ label = 'הרשמות להדרכות  ::  public' } }
                parameters = [ordered]@{
                    __IMTCONN__ = [ordered]@{
                        data = [ordered]@{ scoped = 'true'; connection = 'monday' }
                        label = 'nataliconectionmonday (plan-t-company - natali koifman)'
                    }
                }
            }
            parameters = @(
                [ordered]@{ name = '__IMTCONN__'; type = 'account:monday'; label = 'Connection'; required = $true }
            )
        }
        parameters = [ordered]@{ __IMTCONN__ = 9828370 }
    }
}

function New-MondayChangeDatesModule {
    param(
        [int]$Id,
        [int]$X,
        [string]$Name
    )

    return [ordered]@{
        id = $Id
        mapper = [ordered]@{
            itemId = '{{30.id}}'
            boardId = '5099813594'
            columnValuesToChange = @(
                [ordered]@{
                    columnId = 'date_mm50qbrx'
                    columnValue = [ordered]@{
                        date = '{{formatDate(get(first(get(first(get(42.data; "days")); "spots")); "start_time"); "YYYY-MM-DDTHH:mm:ss"; "Asia/Jerusalem")}}'
                        includeTime = $true
                    }
                },
                [ordered]@{
                    columnId = 'date_mm50szvs'
                    columnValue = [ordered]@{
                        date = '{{formatDate(now; "YYYY-MM-DDTHH:mm:ss"; "Asia/Jerusalem")}}'
                        includeTime = $true
                    }
                }
            )
            create_labels_if_missing = $false
        }
        module = 'monday:ChangeMultipleColumnValues'
        version = 1
        metadata = [ordered]@{
            designer = [ordered]@{ x = $X; y = 0; name = $Name }
            restore = [ordered]@{
                expect = [ordered]@{
                    boardId = [ordered]@{ mode = 'edit'; label = 'הרשמות להדרכות  ::  public' }
                    columnValuesToChange = [ordered]@{
                        mode = 'chose'
                        items = @(
                            [ordered]@{
                                columnId = [ordered]@{ mode = 'chose'; label = 'תאריך הדרכה' }
                                columnValue = [ordered]@{ nested = [ordered]@{ includeTime = [ordered]@{ mode = 'chose' } } }
                            },
                            [ordered]@{
                                columnId = [ordered]@{ mode = 'chose'; label = 'תאריך הרשמה' }
                                columnValue = [ordered]@{ nested = [ordered]@{ includeTime = [ordered]@{ mode = 'chose' } } }
                            }
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
            parameters = @(
                [ordered]@{ name = '__IMTCONN__'; type = 'account:monday'; label = 'Connection'; required = $true }
            )
        }
        parameters = [ordered]@{ __IMTCONN__ = 9828370 }
    }
}

function New-HttpGetModule {
    param(
        [int]$Id,
        [string]$Url,
        [int]$X,
        [string]$Name
    )

    return [ordered]@{
        id = $Id
        mapper = [ordered]@{
            url = $Url
            serializeUrl = $false
            method = 'get'
            headers = @(
                [ordered]@{ name = 'Accept'; value = 'application/json' }
            )
            qs = @()
            bodyType = ''
            parseResponse = $true
            authUser = ''
            authPass = ''
            timeout = ''
            shareCookies = $false
            ca = ''
            rejectUnauthorized = $true
            followRedirect = $true
            followAllRedirects = $false
            useQuerystring = $false
            gzip = $true
            useMtls = $false
        }
        module = 'http:ActionSendData'
        version = 3
        metadata = [ordered]@{
            designer = [ordered]@{ x = $X; y = 0; name = $Name }
            restore = [ordered]@{
                expect = [ordered]@{
                    method = [ordered]@{ mode = 'chose'; label = 'GET' }
                    headers = [ordered]@{ mode = 'chose'; items = @(1) }
                    qs = [ordered]@{ mode = 'chose' }
                    bodyType = [ordered]@{ label = 'Empty' }
                }
            }
        }
        parameters = [ordered]@{
            handleErrors = $false
            useNewZLibDeCompress = $true
        }
    }
}

$webhook = Copy-Module -Id 1
$createItem = Copy-Module -Id 30
$emailHtmlVariable = Copy-Module -Id 12
$sendEmail = Copy-Module -Id 2

$configItem = New-MondayGetItemModule -Id 39 -ItemId '3076389232' -X 300 -Name 'Monday - קריאת הגדרת ההדרכה הפעילה'
$activeCalendlyLink = 'first(map(39.column_values; "text"; "id"; "text_mm578mx0"))'
$schedulingLink = New-HttpGetModule -Id 40 -X 600 -Name 'Calendly - קריאת הקישור הפעיל' -Url ('https://calendly.com/api/booking/scheduling_links/{{get(split(' + $activeCalendlyLink + '; "/"); 5)}}')
$eventType = New-HttpGetModule -Id 41 -X 900 -Name 'Calendly - קריאת פרטי ההדרכה' -Url 'https://calendly.com/api/booking/event_types/lookup?share_uuid={{40.data.owner_uuid}}'
$eventRange = New-HttpGetModule -Id 42 -X 1200 -Name 'Calendly - קריאת תאריך ושעת ההדרכה' -Url 'https://calendly.com/api/booking/event_types/{{41.data.uuid}}/calendar/range?timezone=Asia%2FJerusalem&diagnostics=false&range_start={{41.data.start_date}}&range_end={{41.data.end_date}}&scheduling_link_uuid={{40.data.uid}}'

$createItem.metadata.designer.x = 1500
$createItem.metadata.designer.y = 0
$createItem.metadata.designer | Add-Member -NotePropertyName name -NotePropertyValue 'Monday - יצירת הרשמה עם המועד שנקבע' -Force
$createItem.mapper.columnIds = @(
    'email_mm50jkhy',
    'phone_mm50904s',
    'color_mm50rkbq',
    'text_mm50vwsm',
    'text_mm578mx0'
)
$createItem.mapper.columnValues.PSObject.Properties.Remove('date_mm50qbrx')
$createItem.mapper.columnValues.PSObject.Properties.Remove('date_mm50szvs')
$createItem.mapper.columnValues | Add-Member -NotePropertyName text_mm578mx0 -NotePropertyValue ('{{' + $activeCalendlyLink + '}}') -Force

$updateDates = New-MondayChangeDatesModule -Id 44 -X 1800 -Name 'Monday - עדכון תאריך ההדרכה ותאריך ההרשמה'
$createdItem = New-MondayGetItemModule -Id 43 -ItemId '{{30.id}}' -X 2100 -Name 'Monday - קריאת כתובת המייל מהפריט שנוצר'

$startTime = 'get(first(get(first(get(42.data; "days")); "spots")); "start_time")'
$zoomUrl = 'https://us06web.zoom.us/j/84959005671'
$googleCalendarUrl = 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=%D7%94%D7%93%D7%A8%D7%9B%D7%AA%20%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA%20PLAN-T&dates={{formatDate(' + $startTime + '; "YYYYMMDDTHHmmss[Z]"; "UTC")}}/{{formatDate(addMinutes(' + $startTime + '; 45); "YYYYMMDDTHHmmss[Z]"; "UTC")}}&details=%D7%A7%D7%99%D7%A9%D7%95%D7%A8%20%D7%9C%D7%94%D7%93%D7%A8%D7%9B%D7%94%3A%20https%3A%2F%2Fus06web.zoom.us%2Fj%2F84959005671&location=Zoom'
$outlookCalendarUrl = 'https://outlook.office.com/calendar/0/deeplink/compose?subject=%D7%94%D7%93%D7%A8%D7%9B%D7%AA%20%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA%20PLAN-T&startdt={{formatDate(' + $startTime + '; "YYYY-MM-DDTHH:mm:ss[Z]"; "UTC")}}&enddt={{formatDate(addMinutes(' + $startTime + '; 45); "YYYY-MM-DDTHH:mm:ss[Z]"; "UTC")}}&body=%D7%A7%D7%99%D7%A9%D7%95%D7%A8%20%D7%9C%D7%94%D7%93%D7%A8%D7%9B%D7%94%3A%20https%3A%2F%2Fus06web.zoom.us%2Fj%2F84959005671&location=Zoom'

$emailHtml = @"
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f5f7fb;direction:rtl;text-align:right;font-family:Arial,Helvetica,sans-serif;color:#111827;line-height:1.7;">
  <div style="max-width:600px;margin:0 auto;padding:24px 14px;">
    <div style="background:#ffffff;border:1px solid #e5eaf0;border-radius:8px;padding:26px 24px;">
      <img src="https://natali6582.github.io/monthly-registration/assets/plan-t-logo.jpg" alt="PLAN-T" width="72" style="display:block;width:72px;max-width:72px;height:auto;border:0;margin:0 0 18px auto;">
      <p style="margin:0 0 14px;font-size:15px;">שלום {{43.name}},</p>
      <p style="margin:0 0 14px;font-size:15px;">תודה על ההרשמה להדרכה במערכת <strong>PLAN-T</strong>. הרשמתך הושלמה והמועד נקבע מראש.</p>
      <p style="margin:0 0 10px;font-size:15px;">מועד ההדרכה:</p>
      <div style="margin:0 0 18px;padding:14px 16px;background:#eef7fb;border-right:4px solid #0b87a5;color:#0f2430;font-weight:700;">{{formatDate($startTime; "DD/MM/YYYY HH:mm"; "Asia/Jerusalem")}} (שעון ישראל)</div>
      <p style="margin:0 0 16px;font-size:15px;">אין צורך לבחור מועד. ניתן להיכנס להדרכה באמצעות הקישור הבא:</p>
      <div style="margin:0 0 18px;text-align:center;">
        <a href="$zoomUrl" style="display:inline-block;background:#0b87a5;color:#ffffff;text-decoration:none;padding:11px 22px;border-radius:6px;font-weight:700;">כניסה להדרכה ב-Zoom</a>
      </div>
      <p style="margin:0 0 10px;font-size:14px;color:#4b5563;">שמירת המועד ביומן:</p>
      <div style="margin:0 0 18px;text-align:center;">
        <a href="$googleCalendarUrl" style="display:inline-block;margin:0 4px 8px;padding:9px 14px;border:1px solid #cbd5e1;color:#111827;text-decoration:none;border-radius:6px;font-weight:700;font-size:14px;">Google Calendar</a>
        <a href="$outlookCalendarUrl" style="display:inline-block;margin:0 4px 8px;padding:9px 14px;border:1px solid #cbd5e1;color:#111827;text-decoration:none;border-radius:6px;font-weight:700;font-size:14px;">Outlook / Apple</a>
      </div>
      <p style="margin:0 0 14px;color:#4b5563;font-size:14px;">לשאלות ניתן לפנות אלינו: <a href="mailto:supportclient@plan-t.org.il" style="color:#006ba6;font-weight:700;text-decoration:none;">supportclient@plan-t.org.il</a></p>
      <div style="margin-top:22px;padding-top:14px;border-top:1px solid #e5e7eb;"><strong>צוות PLAN-T</strong><br><span style="color:#4b5563;font-size:14px;">PLAN-T Smart Financial Platform</span></div>
    </div>
  </div>
</body>
</html>
"@

$emailHtmlVariable.metadata.designer.x = 2400
$emailHtmlVariable.metadata.designer.y = 0
$emailHtmlVariable.metadata.designer | Add-Member -NotePropertyName name -NotePropertyValue 'בניית מייל אישור עם מועד וקישור' -Force
$emailHtmlVariable.mapper.name = 'Registration_Email_HTML'
$emailHtmlVariable.mapper.scope = 'roundtrip'
$emailHtmlVariable.mapper.value = $emailHtml

$sendEmail.metadata.designer.x = 2700
$sendEmail.metadata.designer.y = 0
$sendEmail.metadata.designer | Add-Member -NotePropertyName name -NotePropertyValue 'שליחת אישור הרשמה לכתובת מהלוח' -Force
$sendEmail.mapper.content = '{{12.Registration_Email_HTML}}'
$sendEmail.mapper.subject = 'ההרשמה שלך להדרכת PLAN-T הושלמה'
$sendEmail.mapper.contentType = 'html'
$sendEmail.mapper.toRecipients = @(
    [ordered]@{
        name = '{{43.name}}'
        address = '{{first(map(43.column_values; "text"; "id"; "email_mm50jkhy"))}}'
    }
)
$sendEmail.mapper.singleValueExtendedProperties = [ordered]@{}

$blueprint.name = 'הרשמה להדרכה חודשית (נטלי) - Wix-Monday-Calendly'
$blueprint.flow = @(
    $webhook,
    $configItem,
    $schedulingLink,
    $eventType,
    $eventRange,
    $createItem,
    $updateDates,
    $createdItem,
    $emailHtmlVariable,
    $sendEmail
)
$blueprint.metadata.designer.orphans = @()

$outputDirectory = Split-Path -Parent $OutputBlueprint
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

$json = ConvertTo-Json -InputObject $blueprint -Depth 100 -Compress
[System.IO.File]::WriteAllText(
    $OutputBlueprint,
    $json,
    [System.Text.UTF8Encoding]::new($false)
)
