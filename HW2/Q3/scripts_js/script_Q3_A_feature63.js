var w = 900;
var h = 500;
var padding = 50;
var feature63 = [];
d3.csv('diabetes.csv', 
    function(d) {
        return { pregnant_times: +d.pregnant_times,
                 plasma_glucose: +d.plasma_glucose,
                 blood_pressure: +d.blood_pressure,
                 skin_thickness: +d.skin_thickness,
                 insulin:        +d.insulin,
                 bmi:            +d.bmi,
                 pedigree:       +d.pedigree,
                 age:            +d.age,
                 class:          +d.class,};
                },
    function(error, rows) {
        rows.map(function(d) {
            feature63.push([d.bmi, d.blood_pressure, d.class]);
                             });
        var xmax = d3.max(feature63, function(d) { return d[0]; });
        var xmin = d3.min(feature63, function(d) { return d[0]; });
        var ymax = d3.max(feature63, function(d) { return d[1]; });
        var ymin = d3.min(feature63, function(d) { return d[1]; });

        var xscale = d3.scale.linear()
                             .domain([xmin, xmax])
                             .range([padding*2, w-padding]);
        var yscale = d3.scale.linear()
                             .domain([ymin, ymax])
                             .range([h-padding, padding]);
        var rscale = d3.scale.linear()
                       .domain([xmin, xmax])
                       .range([3, 3]);

        var mysvg = d3.select('#A_feature63')
                      .append('svg')
                      .attr('width', w)
                      .attr('height', h);

        var feature63_nt = feature63.filter(function(d) {
                                 return d[2] == 0; });
        feature63_nt.push([3, 117]);

        var feature63_pt = feature63.filter(function(d) {
                                 return d[2] == 1; });
        feature63_pt.push([3, 110]);

        var circles = mysvg.selectAll('circle')
                           .data(feature63_nt)
                           .enter()
                           .append('circle');
        circles.attr('cx', function(d) { return xscale(d[0]); })
               .attr('cy', function(d) { return yscale(d[1]); })
               .attr('r', function(d) { return rscale(d[0]); })
               .attr('stroke', 'rgb(0, 0, 255)')
               .attr('stroke-width', '1')
               .attr('fill', 'none');

        var triangles = mysvg.selectAll('polygon')
                             .data(feature63_pt)
                             .enter()
                             .append('polygon');
        triangles.attr('points', function(d) {
            var point1 = [xscale(d[0]) - 2*Math.sqrt(3), yscale(d[1]) + 2].join(',');
            var point2 = [xscale(d[0]), yscale(d[1]) - 4].join(',');
            var point3 = [xscale(d[0]) + 2*Math.sqrt(3), yscale(d[1]) + 2].join(',');
            return [point1, point2, point3].join(' ');
                                             })
                 .attr('stroke', 'rgb(255, 0, 0)')
                 .attr('stroke-width', '1')
                 .attr('fill', 'none');

        var xAxis = d3.svg.axis()
                      .scale(xscale)
                      .orient('bottom');
        mysvg.append('g')
             .attr('class', 'axis')
             .attr('transform', 'translate(0,' + (h - padding) + ')')
             .call(xAxis);

        var yAxis = d3.svg.axis()
                      .scale(yscale)
                      .orient('left');
        mysvg.append('g')
             .attr('class', 'axis')
             .attr('transform', 'translate(' + padding*2 + ',0)')
             .call(yAxis);

        mysvg.append('text')                // Figure Title
             .attr('x', (w + padding) / 2)
             .attr('y', padding / 2)
             .attr('text-anchor', 'middle')  
             .style('font-size', '24px') 
             .text('BMI vs. Blood Pressure');
        mysvg.append('text')                // Figure Legend
             .attr('x', xscale(4))
             .attr('y', yscale(115))
             .attr('text-anchor', 'left')  
             .style('font-size', '16px') 
             .text('Negative');
        mysvg.append('text')                // Figure Legend
             .attr('x', xscale(4))
             .attr('y', yscale(108))
             .attr('text-anchor', 'left')  
             .style('font-size', '16px') 
             .text('Positive');
        mysvg.append('text')                // X Label
             .attr('x', (w + padding) / 2)
             .attr('y', h - padding / 10)
             .attr('text-anchor', 'middle')  
             .style('font-size', '20px') 
             .text('BMI');
        mysvg.append('text')                // Y Label
             .attr('y', padding*1.2)
             .attr('x', - h / 2)
             .attr('transform', 'rotate(-90)')
             .attr('text-anchor', 'middle')  
             .style('font-size', '20px') 
             .text('Blood Pressure');
       });