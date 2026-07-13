param(
    [Parameter(Mandatory = $true)]
    [string]$BlueprintResponsePath,

    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'

$source = Get-Content -LiteralPath $BlueprintResponsePath -Raw -Encoding UTF8 | ConvertFrom-Json

if ($source.response.blueprint) {
    $blueprint = $source.response.blueprint
} elseif ($source.blueprint) {
    $blueprint = $source.blueprint
} else {
    throw 'Blueprint response does not contain a blueprint.'
}

$emailModule = @($blueprint.flow | Where-Object { $_.id -eq 12 })
if ($emailModule.Count -ne 1) {
    throw "Expected one module with ID 12, found $($emailModule.Count)."
}

$startTime = '42.data.days[1].spots[1].start_time'
$zoomUrl = 'https://us06web.zoom.us/j/84959005671'

# Hebrew is encoded as HTML entities so the generated email is independent of
# the script file's character encoding. Email clients render normal Hebrew.
$emailHtml = @"
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f5f7fb;direction:rtl;text-align:right;font-family:Arial,Helvetica,sans-serif;color:#111827;line-height:1.7;">
  <div style="max-width:600px;margin:0 auto;padding:24px 14px;">
    <div style="background:#ffffff;border:1px solid #e5eaf0;border-radius:8px;padding:26px 24px;">
      <img src="https://natali6582.github.io/monthly-registration/assets/plan-t-logo.jpg" alt="PLAN-T" width="72" style="display:block;width:72px;max-width:72px;height:auto;border:0;margin:0 0 18px auto;">
      <p style="margin:0 0 14px;font-size:15px;">&#1513;&#1500;&#1493;&#1501;,</p>
      <p style="margin:0 0 18px;font-size:15px;">&#1514;&#1493;&#1491;&#1492; &#1506;&#1500; &#1492;&#1492;&#1512;&#1513;&#1502;&#1492; &#1500;&#1492;&#1491;&#1512;&#1499;&#1492; &#1489;&#1502;&#1506;&#1512;&#1499;&#1514; <strong>PLAN-T</strong>. &#1492;&#1512;&#1513;&#1502;&#1514;&#1498; &#1492;&#1493;&#1513;&#1500;&#1502;&#1492; &#1493;&#1492;&#1502;&#1493;&#1506;&#1491; &#1504;&#1511;&#1489;&#1506; &#1502;&#1512;&#1488;&#1513;.</p>
      <p style="margin:0 0 8px;font-size:15px;">&#1502;&#1493;&#1506;&#1491; &#1492;&#1492;&#1491;&#1512;&#1499;&#1492;:</p>
      <p style="margin:0 0 18px;font-size:15px;"><strong>{{formatDate($startTime; "DD/MM/YYYY HH:mm"; "Asia/Jerusalem")}} (&#1513;&#1506;&#1493;&#1503; &#1497;&#1513;&#1512;&#1488;&#1500;)</strong></p>
      <p style="margin:0 0 12px;font-size:15px;">&#1504;&#1497;&#1514;&#1503; &#1500;&#1492;&#1497;&#1499;&#1504;&#1505; &#1500;&#1492;&#1491;&#1512;&#1499;&#1492; &#1489;&#1488;&#1502;&#1510;&#1506;&#1493;&#1514; &#1492;&#1511;&#1497;&#1513;&#1493;&#1512; &#1492;&#1489;&#1488;:</p>
      <div style="margin:0 0 20px;text-align:center;">
        <a href="$zoomUrl" style="display:inline-block;background:#0b87a5;color:#ffffff;text-decoration:none;padding:11px 22px;border-radius:6px;font-weight:700;">&#1499;&#1504;&#1497;&#1505;&#1492; &#1500;&#1492;&#1491;&#1512;&#1499;&#1492; &#1489;-Zoom</a>
      </div>
      <p style="margin:0 0 10px;font-size:15px;">&#1513;&#1502;&#1497;&#1512;&#1514; &#1492;&#1502;&#1493;&#1506;&#1491; &#1489;&#1497;&#1493;&#1502;&#1503;:</p>
      <div style="margin:0 0 20px;text-align:center;">
        <a href="https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=%D7%94%D7%93%D7%A8%D7%9B%D7%AA%20%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA%20PLAN-T&amp;dates={{formatDate($startTime; "YYYYMMDDTHHmmss[Z]"; "UTC")}}/{{formatDate(addMinutes($startTime; 45); "YYYYMMDDTHHmmss[Z]"; "UTC")}}&amp;details=%D7%A7%D7%99%D7%A9%D7%95%D7%A8%20%D7%9C%D7%94%D7%93%D7%A8%D7%9B%D7%94%3A%20https%3A%2F%2Fus06web.zoom.us%2Fj%2F84959005671&amp;location=Zoom" style="display:inline-block;margin:0 4px 8px;padding:9px 14px;border:1px solid #cbd5e1;color:#111827;text-decoration:none;border-radius:6px;font-weight:700;font-size:14px;">Google Calendar</a>
        <a href="https://outlook.office.com/calendar/0/deeplink/compose?subject=%D7%94%D7%93%D7%A8%D7%9B%D7%AA%20%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA%20PLAN-T&amp;startdt={{formatDate($startTime; "YYYY-MM-DDTHH:mm:ss[Z]"; "UTC")}}&amp;enddt={{formatDate(addMinutes($startTime; 45); "YYYY-MM-DDTHH:mm:ss[Z]"; "UTC")}}&amp;body=%D7%A7%D7%99%D7%A9%D7%95%D7%A8%20%D7%9C%D7%94%D7%93%D7%A8%D7%9B%D7%94%3A%20https%3A%2F%2Fus06web.zoom.us%2Fj%2F84959005671&amp;location=Zoom" style="display:inline-block;margin:0 4px 8px;padding:9px 14px;border:1px solid #cbd5e1;color:#111827;text-decoration:none;border-radius:6px;font-weight:700;font-size:14px;">Outlook / Apple</a>
      </div>
      <p style="margin:0 0 18px;color:#4b5563;font-size:14px;">&#1500;&#1513;&#1488;&#1500;&#1493;&#1514; &#1504;&#1497;&#1514;&#1503; &#1500;&#1508;&#1504;&#1493;&#1514; &#1488;&#1500;&#1497;&#1504;&#1493;: <a href="mailto:supportclient@plan-t.org.il" style="color:#006ba6;font-weight:700;text-decoration:none;">supportclient@plan-t.org.il</a></p>
      <div style="margin-top:22px;padding-top:14px;border-top:1px solid #e5e7eb;"><strong>&#1510;&#1493;&#1493;&#1514; PLAN-T</strong><br><span style="color:#4b5563;font-size:14px;">PLAN-T Smart Financial Platform</span></div>
    </div>
  </div>
</body>
</html>
"@

$emailModule[0].mapper.value = $emailHtml.Trim()

$patchRequest = [ordered]@{
    blueprint = ($blueprint | ConvertTo-Json -Depth 80 -Compress)
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$utf8NoBom = [Text.UTF8Encoding]::new($false)

[IO.File]::WriteAllText(
    (Join-Path $OutputDirectory 'email-copy-blueprint.json'),
    ($blueprint | ConvertTo-Json -Depth 80 -Compress),
    $utf8NoBom
)

[IO.File]::WriteAllText(
    (Join-Path $OutputDirectory 'email-copy-patch-request.json'),
    ($patchRequest | ConvertTo-Json -Depth 85 -Compress),
    $utf8NoBom
)

[ordered]@{
    moduleId = 12
    dynamicStartTime = $startTime
    zoomUrl = $zoomUrl
    outputDirectory = (Resolve-Path $OutputDirectory).Path
} | ConvertTo-Json -Compress
