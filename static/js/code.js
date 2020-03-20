
google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {

      var data = df['product']([
        ['City', '2010 Population',],
        ['Radio', 3],
        ['Pot', 3],
        ['Slipper', 1],
        ['Bag', 1],
        ['Belt', 2]
        ['Bulp', 2]
        ['Laptop', 1]
        ['Fish tank', 2]
        ['Spoon', 1]
        ['Vaccum Cleaner', 1]
        ['Cupboard', 2]
        ['Shoes', 1]
        ['Chips',1]
      ]);

      var options = {
        title: 'Population of Largest U.S. Cities',
        chartArea: {width: '50%'},
        hAxis: {
          title: 'Total Population',
          minValue: 0
        },
        vAxis: {
          title: 'City'
        }
      };

      var chart = new google.visualization.BarChart(document.getElementById('chart_div'));

      chart.draw(data, options);
    }