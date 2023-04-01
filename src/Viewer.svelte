<script lang="ts">
    import type {ChartConfiguration, ChartData, ChartItem} from 'chart.js'
    import {
        Chart as ChartJS,
        Colors,
        Legend,
        LinearScale,
        LineController,
        LineElement,
        PointElement,
        TimeScale,
        Tooltip
    } from 'chart.js'

    import {DateTime} from 'luxon'
    import 'chartjs-adapter-luxon'

    import {onMount} from 'svelte'

    import {data} from './data'

    // register chart elements
    ChartJS.register(
        Colors,
        Legend,
        LinearScale,
        LineController,
        LineElement,
        PointElement,
        TimeScale,
        Tooltip
    )

    /**
     * The chart canvas element.
     */
    let chartElement: ChartItem

    /**
     * Returns the chart data.
     */
    function getChartData(): ChartData {
        const datapointSets = {
            'Lines': [],
            'Code': [],
            'Comment': [],
            'Blank': [],
        }
        data.forEach(datapoint => {
            const time = DateTime.fromSeconds(datapoint.timestamp).toISO()
            datapointSets['Lines'].push({x: time, y: datapoint.lines})
            datapointSets['Code'].push({x: time, y: datapoint.code})
            datapointSets['Comment'].push({x: time, y: datapoint.comment})
            datapointSets['Blank'].push({x: time, y: datapoint.blank})
        })
        const chartData = {datasets: []}
        Object.keys(datapointSets).forEach(label => chartData.datasets.push({
            label,
            data: datapointSets[label],
            fill: false,
            pointRadius: 0,
            lineTension: 0.05,
        }))
        if (chartData.datasets.length === 0) {
            throw new Error('No data to display')
        }
        return chartData
    }

    /**
     * The chart configuration.
     */
    const chartConfig: ChartConfiguration = {
        type: 'line',
        data: getChartData(),
        options: {
            plugins: {
                title: {
                    display: false
                },
                legend: {
                    display: true
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            hover: {
                mode: 'nearest',
                intersect: false
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'month'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: false
                    }
                }
            }
        }
    }

    // create chart on mount
    onMount(() => {
        new ChartJS(chartElement, chartConfig)
    })
</script>

<canvas bind:this={chartElement}></canvas>
