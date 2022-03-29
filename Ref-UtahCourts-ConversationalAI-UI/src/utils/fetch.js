export async function post(url, jsonToStringify) {
    let options = {
        method: "POST",
        body: JSON.stringify(jsonToStringify),
        headers: {
            "Content-Type": "application/json",
        },
    }; 
    let response = await fetch(url, options);
    return await response.json()
}