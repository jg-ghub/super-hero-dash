const chart_layout = {
    autosize: false,
    width: 480,
    height: 640,
    margin: {
        l: 80,
        r: 50,
        b: 100,
        t: 100,
        pad: 4
    },
    title: {
        text:'Super Hero Powers',
        font: {
          family: 'Courier New, monospace',
          size: 24
        },
        xref: 'paper',
        x: 0.05,
      },
      xaxis: {
        title: {
          text: 'Power Ratings',
          font: {
            family: 'Courier New, monospace',
            size: 18,
            color: '#7f7f7f'
          }
        }
      }
};

$(document).ready(() => {
    let resp = $.get('/api/v1/resources/heros/all',
        (err, req, resp) => {
            let rs = resp['responseJSON'];
            let data = rs.map(d => {return {id: d.id, text:d.name}});
            $("#search-dropdown").select2({data: data});
            console.log($("#search-dropdown").select2('val'));
        }
    )
    
    $('#search').click(() => {
        let id = $("#search-dropdown").val();
        let name = $("#search-dropdown :selected").text();
        $('#hero-title').text(name);
        
        $.get(`/api/v1/resources/heros/image?id=${id}`,
            (err, req, resp) => {
                $('#hero-img').attr('src', resp['responseJSON']['url']);
            }
        );

        $.get(`/api/v1/resources/heros/occupation?id=${id}`,
            (err, req, resp) => {
                $('#hero-occupation').text(resp['responseJSON']['occupation']);
            }
        );

        $.get(`/api/v1/resources/heros/powerstats?id=${id}`,
            (err, req, resp) => {
                let rs = resp['responseJSON'];
                let data = [{
                    type: 'bar',
                    x: [rs.intelligence, rs.strength, rs.speed, rs.durability, rs.power, rs.combat],
                    y: ['inteligence', 'strength', 'speed', 'durability', 'power', 'combat'],
                    orientation: 'h'
                }];
                Plotly.newPlot('hero-bar-chart', data, chart_layout);
            }
        );
    });
});