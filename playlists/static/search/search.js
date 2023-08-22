function createSlider(elementId, lowerValueId, upperValueId) {
    var slider = document.getElementById(elementId);

    // If the slider element is not present, return
    if (!slider) {
        return;
    }

    noUiSlider.create(slider, {
        start: [20, 80],
        connect: true,
        range: {
            'min': 0,
            'max': 100
        }
    });

    var lowerValue = document.getElementById(lowerValueId);
    var upperValue = document.getElementById(upperValueId);

    // Function to update the displayed slider values
    function updateValues() {
        var values = slider.noUiSlider.get();
        lowerValue.textContent = Math.round(values[0]);
        upperValue.textContent = Math.round(values[1]);
    }

    // Listen for slide event to adjust the value position
    slider.noUiSlider.on('update', updateValues);

    // Initial value set
    updateValues();
}

// Create sliders for Danceability, Energy, and Valence
createSlider('danceabilitySlider', 'danceabilityLowerValue', 'danceabilityUpperValue');
createSlider('energySlider', 'energyLowerValue', 'energyUpperValue');
createSlider('valenceSlider', 'valenceLowerValue', 'valenceUpperValue');
