document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#locationForm');

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent page refresh
            console.log('Form submitted!');
            const postcode = document.querySelector('.postcode').value;
            if (postcode.length == 5){
                getLatLon(postcode).then(coords => {
                    if (coords) {
                        saveCoordinatesToFile(coords.latitude, coords.longitude);
                    }
                }); // { latitude: "40.7507", longitude: "-73.9964" }
            } else {
                let [latitude, longitude] = postcode.split(" ");
                saveCoordinatesToFile(latitude, coords.longitude);
            }
        });
    } else {
        console.error('Form not found!');
    }
});

async function getLatLon(zip) {
    const url = `https://api.zippopotam.us/us/${zip}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Invalid ZIP Code");

        const data = await response.json();
        const { latitude, longitude } = data.places[0];

        return { latitude: latitude.toString(), longitude: longitude.toString() }; // Return as strings
    } catch (error) {
        console.error("Error:", error.message);
        return null;
    }
}

function saveCoordinatesToFile(latitude, longitude) {
    const data = { latitude, longitude };
    fetch('/save-coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        console.log('Coordinates saved:', result);
    })
    .catch(error => {
        console.error('Error saving coordinates:', error);
    });
}
