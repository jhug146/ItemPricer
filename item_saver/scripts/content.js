
const LOCALHOST = "http://127.0.0.1:8000";
const URL = window.location.href;
const VINTED_ID_REGEX = new RegExp("(?<=/)(.{10})(?=-)");

async function savePage() {
    const vinted_id = URL.match(VINTED_ID_REGEX);
    if (vinted_id.length > 0) {
        const response = await fetch(
            LOCALHOST + "/listener/new_item/",
            {
                method: "POST",
                body: JSON.stringify({
                    "vinted_id": vinted_id[0],
                    "url": URL,
                    "is_bought": "NO"
                })
            }
        ).then(
            res => console.log(res.text())
        ).catch(
            error => alert(error)
        );
    } else {
        alert("Can't parse Vinted ID from URL");
    }
}

savePage();
