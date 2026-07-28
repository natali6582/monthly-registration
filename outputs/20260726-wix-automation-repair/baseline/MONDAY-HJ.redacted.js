// Redacted baseline captured from Wix Automation 193c589f-1b2f-4d22-a105-e2d475c7b71f.
// The compromised Monday token was intentionally not copied.
import { fetch } from 'wix-fetch';

export async function createMondayItem(formData) {
  const API_KEY = "REDACTED_COMPROMISED_TOKEN";
  const BOARD_ID = 5099813594;
  const GROUP_ID = "group_mm50r2qx";

  const columnValues = JSON.stringify({
    "phone_mm50904s":  { "phone": formData['field:phone'] || "", "countryShortName": "IL" },
    "email_mm50jkhy":  { "email": formData['field:email'] || "", "text": formData['field:email'] || "" },
    "text_mm50vwsm":   formData['field:company'] || "",
    "date_mm50szvs":   { "date": new Date().toISOString().split("T")[0] },
    "color_mm50rkbq":  { "index": 7 }
  });

  const mutation = `
    mutation {
      create_item(
        board_id: ${BOARD_ID},
        group_id: "${GROUP_ID}",
        item_name: "${formData['field:fullName']}",
        column_values: ${JSON.stringify(columnValues)}
      ) {
        id
        name
      }
    }
  `;

  const response = await fetch("https://api.monday.com/v2", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": API_KEY
    },
    body: JSON.stringify({ query: mutation })
  });

  const result = await response.json();
  console.log("Monday item created:", result);
  return result;
}
