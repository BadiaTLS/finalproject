function developClusteringModel(x_values, y_values, k) {
    // Combine x_values and y_values into a single data array
    let data = [];
    for (let i = 0; i < x_values.length; i++) {
        data.push([x_values[i], y_values[i]]);
    }

    // Perform k-means clustering
    let result = kMeansClustering(data, k);

    // Plot the chart
    plotClusteringChart(data, result.centroids);

    // Write the number of iterations to the screen
    document.getElementById("iterations").innerHTML =
        "<b>Number of Iterations: </b> " + String(result.iterations);
}

function kMeansClustering(data, k) {
    // Step 1: Initialize centroids randomly
    let centroids = [];
    for (let i = 0; i < k; i++) {
        centroids.push(data[Math.floor(Math.random() * data.length)]);
    }

    let oldCentroids;
    let iterations = 0;
    do {
        // Step 2: Assign points to nearest centroid
        let clusters = {};
        for (let i = 0; i < data.length; i++) {
            let distances = [];
            for (let j = 0; j < k; j++) {
                distances.push(euclideanDistance(data[i], centroids[j]));
            }
            let clusterIndex = distances.indexOf(Math.min(...distances));
            if (!clusters[clusterIndex]) {
                clusters[clusterIndex] = [];
            }
            clusters[clusterIndex].push(data[i]);
        }

        // Step 3: Update centroid location
        oldCentroids = [...centroids];
        for (let i = 0; i < k; i++) {
            let clusterData = clusters[i];
            let newCentroid = [];
            for (let j = 0; j < clusterData[0].length; j++) {
                let sum = 0;
                for (let l = 0; l < clusterData.length; l++) {
                    sum += clusterData[l][j];
                }
                newCentroid.push(sum / clusterData.length);
            }
            centroids[i] = newCentroid;
        }

        iterations++;
    } while (!hasConverged(oldCentroids, centroids) && iterations < 100);

    return { centroids, iterations };
}

function euclideanDistance(point1, point2) {
    let sum = 0;
    for (let i = 0; i < point1.length; i++) {
        sum += Math.pow(point1[i] - point2[i], 2);
    }
    return Math.sqrt(sum);
}

function hasConverged(oldCentroids, centroids) {
    for (let i = 0; i < oldCentroids.length; i++) {
        if (euclideanDistance(oldCentroids[i], centroids[i]) > 0.0001) {
            return false;
        }
    }
    return true;
}

function plotClusteringChart(data, centroids) {
    let ctx = document.getElementById("clusteringChart").getContext("2d");

    // Assign points to nearest centroid
    let clusters = {};
    for (let i = 0; i < data.length; i++) {
        let distances = [];
        for (let j = 0; j < centroids.length; j++) {
            distances.push(euclideanDistance(data[i], centroids[j]));
        }
        let clusterIndex = distances.indexOf(Math.min(...distances));
        if (!clusters[clusterIndex]) {
            clusters[clusterIndex] = [];
        }
        clusters[clusterIndex].push({ x: data[i][0], y: data[i][1] });
    }

    // Create datasets for each cluster
    let datasets = [];
    let colors = [
        "rgba(255,99,132,0.6)",
        "rgba(54,162,235,0.6)",
        "rgba(255,206,86,0.6)",
        "rgba(75,192,192,0.6)",
        "rgba(153,102,255,0.6)",
        "rgba(255,159,64,0.6)"
    ];
    for (let i = 0; i < Object.keys(clusters).length-1; i++) {
        datasets.push({
            label: "Cluster " + (i + 1),
            data: clusters[i],
            backgroundColor: colors[i % colors.length],
            borderColor: colors[i % colors.length],
            borderWidth: 1, 
            pointRadius: 5,
        });
    }

    // Add centroids to datasets
    let centroidPoints = [];
    for (let i = 0; i < centroids.length; i++) {
        centroidPoints.push({ x: centroids[i][0], y: centroids[i][1] });
    }
    datasets.push({
        label: "Centroids",
        data: centroidPoints,
        backgroundColor: "rgba(0,0,0,0.5)",
        borderColor: "rgba(0,0,0,0.7)",
        borderWidth: 1
    });

    // Create chart
    let myChart = new Chart(ctx, {
        type: "scatter",
        data: {
            datasets: datasets
        },
        options: {
            scales: {
                xAxes: [
                    {
                        type: "linear",
                        position: "bottom"
                    }
                ]
            }
        }
    });
}

