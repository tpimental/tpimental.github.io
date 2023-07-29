// Fetch the names from the JSON file
fetch('sorted_names.json')
    .then(response => response.json())
    .then(names => {
        // Get the <ul> element to add the names
        const nameList = document.getElementById('nameList');

        // Loop through the names and create <li> elements for each name
        names.forEach(name => {
            const li = document.createElement('li');
            li.textContent = name;
            nameList.appendChild(li);
        });
    })
    .catch(error => console.error('Error fetching names:', error));
