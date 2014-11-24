$(document).ready(
  function (){
    $('.json').each(function() {
      var th = $(this);
      var txtData = th.text();
      txtData = txtData.slice(0, txtData.length - 4) + "]";
      data = JSON.parse(txtData);
      th.text("");
      th.attr("style", "");

      chart = c3.generate({
        bindto: this,
        color: {
          pattern: ['#007ce0']
        },
        padding: {
          bottom: 20
        },
        data: {
          json: data,
          keys: {
            x: 'code',
            value: ['value']
          },
          x: 'x',
          type: 'bar'
        },
        axis: {
          x: {
            type: 'category',
            tick: {
              rotate: 20
            }
          },
          y: {
            show: true
          }
        },
        grid: {
          y: {
            show: true
          }
        }
      });
      chart.internal.margin2.top=360;
    });

  });