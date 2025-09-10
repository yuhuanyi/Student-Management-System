// 成绩分布柱状图初始化函数
function initScoreDistributionChart() {
    const scoreChart = echarts.init(document.getElementById('score-distribution'));
    scoreChart.setOption({
        title: {
            text: '成绩分布统计',
            textStyle: {
                color: '#333',
                fontSize: 20
            }
        },
        tooltip: {},
        xAxis: {
            data: ['<60', '60 - 70', '70 - 80', '80 - 90', '90 - 100'],
            axisLabel: {
                color: '#666'
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                color: '#666'
            }
        },
        series: [{
            name: '人数',
            type: 'bar',
            data: [5, 20, 45, 25, 5],
            itemStyle: {
                color: '#3498db'
            }
        }]
    });
}

// 专业平均分雷达图初始化函数
function initMajorScoresChart() {
    const majorChart = echarts.init(document.getElementById('major-scores'));
    majorChart.setOption({
        title: {
            text: '专业平均分对比',
            textStyle: {
                color: '#333',
                fontSize: 20
            }
        },
        radar: {
            indicator: [
                { name: '计算机科学', max: 100 },
                { name: '软件工程', max: 100 },
                { name: '人工智能', max: 100 },
                { name: '数据科学', max: 100 }
            ],
            shape: 'circle',
            splitArea: {
                areaStyle: {
                    color: ['rgba(52, 152, 219, 0.1)', 'rgba(52, 152, 219, 0.2)', 'rgba(52, 152, 219, 0.3)', 'rgba(52, 152, 219, 0.4)']
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#666'
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#666'
                }
            }
        },
        series: [{
            type: 'radar',
            data: [
                { value: [85, 82, 88, 90], name: '平均分' }
            ],
            itemStyle: {
                color: '#e74c3c'
            },
            areaStyle: {
                opacity: 0.3
            }
        }]
    });
}

// 页面加载完成后初始化图表
window.onload = function () {
    initScoreDistributionChart();
    initMajorScoresChart();
};