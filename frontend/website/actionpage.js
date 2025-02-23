document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#locationForm');

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent page refresh
            console.log('Form submitted!');
            const postcode = document.querySelector('.postcode').value;
            if (postcode.length == 5){
                getLatLon(postcode).then(coords => console.log(coords)); // { latitude: 40.7507, longitude: -73.9964 }
            } else {
                console.log('Postcode:', postcode);
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

        return { latitude: parseFloat(latitude), longitude: parseFloat(longitude) };
    } catch (error) {
        console.error("Error:", error.message);
        return null;
    }
}

// Example usage
// getPostcodeFromLatLng(51.5074, -0.1278).then(console.log);
