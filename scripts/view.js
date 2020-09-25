const width = 800, height = 600

// tick function
const tick = (e) => {
    node.attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .call(force.drag)

    link.attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
}


const getRadius = (r) => (r / 2.0) + 5
const getRandomColor = () => {
    return all_colors[Math.floor(Math.random() * all_colors.length)]
}

const links = spiderJson.links
const nodes = spiderJson.nodes

// add svg to body

let svg = d3.select('#graph').append('svg')
    .attr('style', 'margin: 30px auto')
    .attr('width', '100%')
    .attr('height', height)

// make force layout in d3
let force = d3.layout.force()
    .size([width, height])
    .nodes(d3.values(nodes))
    .links(links)
    .on('tick', tick) // interacting with the force layout will execute this function
    .linkDistance(300)
    .start()

let link = svg.selectAll('.link')
    .data(links)
    .enter().append('line')
    .attr('class', 'link')

let node = svg.selectAll('.node')
    .data(force.nodes())
    .enter().append('circle')
    .attr('class', 'node')
    .attr('fill', (d) => getRandomColor())
    .attr('r', d => getRadius(d.rank))

// show the url when user hovers over a node
node.append("title")
    .text(d => d.url);


const sortedNodes = nodes.sort((a, b) =>  b.rank - a.rank)

const topRanked = document.getElementById('top-ranked')

sortedNodes.forEach((node, index) => {
    topRanked.innerHTML += `<p>${index + 1}: ${node.url.replace("https://", '')}, Rank = ${node.rank}</p>`
});
