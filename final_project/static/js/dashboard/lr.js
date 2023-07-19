function linearRegression(x_values, y_values) {
    var x_mean = x_values.reduce((a, b) => a + b, 0) / x_values.length;
    var y_mean = y_values.reduce((a, b) => a + b, 0) / y_values.length;

    var slope_numerator = 0;
    var slope_denominator = 0;

    for (var i = 0; i < x_values.length; i++) {
        slope_numerator += (x_values[i] - x_mean) * (y_values[i] - y_mean);
        slope_denominator += Math.pow((x_values[i] - x_mean), 2);
    }

    var slope = slope_numerator / slope_denominator;
    var intercept = y_mean - slope * x_mean;

    return { slope: slope, intercept: intercept };
}

function generatePredictedData(x_values, regressor) {
    var y_hat = [];
    for (var i = 0; i < x_values.length; i++) {
        y_hat.push(x_values[i] * regressor.slope + regressor.intercept);
    }
    return y_hat;
}

function plotRegressionChart(x_values, y_values, x_predictions, y_predictions, regressor, x_valuess, x_predictionss) {
    var all_x_values = x_valuess.concat(x_predictionss);
    var y_hat_values = generatePredictedData(x_values, regressor);
    var y_hat_predictions = generatePredictedData(x_predictions, regressor);

    var ctx = document.getElementById('regressionChart').getContext('2d');

    // Create an array of None values with the same length as x
    let noneArray = new Array(y_hat_values.length-1).fill(null);

    // Concatenate the noneArray and y arrays
    let y_res = noneArray.concat(y_hat_predictions);
    // console.log(y_res)

    var datasets = [{
        type: 'line',
        label: 'True Values Line',
        data: y_hat_values,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)'
    }, {
        type: 'scatter',
        label: 'True Values',
        data: y_values,
        borderColor: 'rgb(0, 0, 0)',
        backgroundColor: 'rgb(0, 0, 0)',
    }, {type: 'line',
    label: 'Predictions Line',
    data: y_res,
    borderColor: 'rgb(110, 255, 132)',
    backgroundColor: 'rgba(110, 255, 132, 0.2)'
}];

    if (typeof window.mixedChart !== 'undefined') {
        window.mixedChart.destroy();
    }

    window.mixedChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: datasets,
            labels: all_x_values, // Use the original date strings for x-axis labels
        },
        options: {
            scales: {
                x: {
                    position: 'bottom',
                },
                y: {
                    beginAtZero: false,
                },
            },
        },
    });
}

function developLrModel(x_values, y_values, x_predictions, y_predictions) {
    var x_values_timestamps = x_values.map((dateStr) => new Date(dateStr).getTime());
    var x_predictions_timestamps = x_predictions.map((dateStr) => new Date(dateStr).getTime());

    var regressor = linearRegression(x_values_timestamps, y_values);
    plotRegressionChart(x_values_timestamps, y_values, x_predictions_timestamps, y_predictions, regressor, x_values, x_predictions);
}

// Test with the provided data and an additional dataset
var x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];
var y_values = [43, 41, 46, 44, 44, 43, 47, 44, 43, 45, 45, 43, 46, 46, 43, 43, 45, 41, 45, 44, 44, 44, 45];

var x_predictions = [24, 25, 26, 27, 28, 29, 30];
var y_predictions = [44, 44, 44, 44, 44, 44, 44];

// developLrModel(x_values, y_values, x_predictions, y_predictions);

var x_values = ["2023-06-19", "2023-06-20", "2023-06-21", "2023-06-22", "2023-06-23", "2023-06-26", "2023-06-27", "2023-06-28", "2023-06-29", "2023-06-30", "2023-07-03", "2023-07-04", "2023-07-05", "2023-07-06", "2023-07-07", "2023-07-10", "2023-07-11", "2023-07-12", "2023-07-13", "2023-07-14", "2023-07-17", "2023-07-18", "2023-07-19"];
var y_values = [43, 41, 46, 44, 44, 43, 47, 44, 43, 45, 45, 43, 46, 46, 43, 43, 45, 41, 45, 44, 44, 44, 45];

var x_predictions = ["2023-07-20", "2023-07-21", "2023-07-22", "2023-07-23", "2023-07-24", "2023-07-25", "2023-07-26"];
var y_predictions = [44, 44, 44, 44, 44, 44, 44];

// developLrModel(x_values, y_values, x_predictions, y_predictions);


