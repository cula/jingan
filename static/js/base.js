function formInit(form) {
    var uri = form.attr('action');
    form.attr('method', 'POST');
    var formGroups = form.find('.form-group');
    var submitWidget = form.find('.form-submit');
    var errBlock = form.find('.form-error-block').last();

    form.validator().submit(function (e) {
      if (!e.isDefaultPrevented()) {
        errBlock.parents('.form-group').removeClass('has-error');
        errBlock.text('');
        var data = form.serialize();
        $.post(uri, data, function(data, textStatus, jqXHR) {
          if (data.errors) {
            var error = data.errors[0];
            errBlock.parents('.form-group').addClass('has-error');
            errBlock.text(error.message);
          } else if (data.redirect) {
            window.location.href = data.redirect;
          } else {
            location.reload();
          }
        });
      }
      return false;
    })
}

function formAjaxSubmit(child, target){
  var form = child.parents('form').first();
  var submitWidget = child;
  var uri = form.attr('action');

  form.validator().submit(function(e){
    if (!e.isDefaultPrevented()) {
      var data = form.serialize();
      $.post(uri, data, function(data, textStatus, jqXHR) {
        if (data.errors) {
          var error = data.errors[0];
          if(error) {
            alert(error.message);
          }
        } else if (data.redirect) {
          $(window.location).attr('href', data.redirect);
        } else {
          location.reload();
        }
      });
    }
    return false;
  })

  form.submit();
}

function doSearch(query) {
  var uri = URI(window.location.href);
  uri.search("").search({q: query});
  window.location.href = uri;
}

function goPage(page) {
  var uri = URI(window.location.href);
  uri.removeSearch("p").addSearch({p: page});
  window.location.href = uri;
}

// for order
function addItem(table) {
  var example = table.find('tr.example').first();
  example.clone().removeClass('example').appendTo(table);
}

$(function () {
  $('.form').each(function() {
    formInit($(this));
  });

  $('[data-toggle="popover"]').popover();

  $('.datetimepicker').datetimepicker({
    language: 'zh-CN',
    todayBtn: 'linked',
    todayHighlight: 'true',
    autoclose: true,
    minView: 2
  });

  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });

  // for order
  var suborders = $('.suborders').first();
  var example = suborders.children('.suborder.example').first();
  var suborderToAdd = example.clone().removeClass('example');
  addItem(suborderToAdd.find('table').first());
  suborderToAdd.appendTo(suborders);

  $('.add-suborder').click(function(){
    var suborderToAdd = example.clone().removeClass('example');
    addItem(suborderToAdd.find('table').first());
    suborderToAdd.appendTo(suborders);
  });

  $('#createOrderForm').validator().submit(function(e){
    if (!e.isDefaultPrevented()) {
      var form = $(this);
      var uri = form.attr('action');
      form.attr('method', 'POST');
      var formGroups = form.find('.form-group');
      var submitWidget = form.find('.form-submit');
      var errBlock = form.find('.form-error-block').last();

      errBlock.parents('.form-group').removeClass('has-error');
      errBlock.text('');
      var data = form.serialize();
      alert(data);
      $.post(uri, data, function(data, textStatus, jqXHR) {
        if (data.errors) {
          var error = data.errors[0];
          errBlock.parents('.form-group').addClass('has-error');
          errBlock.text(error.message);
        } else if (data.redirect) {
          window.location.href = data.redirect;
        } else {
          location.reload();
        }
      });
    }
    return false;
  });

});
