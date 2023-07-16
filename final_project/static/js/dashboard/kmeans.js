function developClusteringModel(data, k) {
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
    let dataPoints = [];
    for (let i = 0; i < data.length; i++) {
        dataPoints.push({ x: data[i][0], y: data[i][1] });
    }
    let centroidPoints = [];
    for (let i = 0; i < centroids.length; i++) {
        centroidPoints.push({ x: centroids[i][0], y: centroids[i][1] });
    }
    let myChart = new Chart(ctx, {
        type: "scatter",
        data: {
            datasets: [
                {
                    label: "Data Points",
                    data: dataPoints,
                    backgroundColor: "rgba(255,99,132,0.2)",
                    borderColor: "rgba(255,99,132,1)",
                    borderWidth: 1
                },
                {
                    label: "Centroids",
                    data: centroidPoints,
                    backgroundColor: "rgba(54,162,235,0.2)",
                    borderColor: "rgba(54,162,235,1)",
                    borderWidth: 1
                }
            ]
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