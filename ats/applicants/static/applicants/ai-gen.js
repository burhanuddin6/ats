$(document).ready(function() {
    add_more();
    add_delete();
  });
  
  function add_form(prefix) {
    var form_idx = $(`#id_${prefix}-TOTAL_FORMS`).val();
    var newel = $(`#${prefix}-empty_form`).html().replace(/__prefix__/g, form_idx);
    var newElParent = $(`<div id="${prefix}-${form_idx}"></div>`);
    newElParent.append(newel);
    $(`#${prefix}-form_set`).append(newElParent);
    $(`#id_${prefix}-TOTAL_FORMS`).val(parseInt(form_idx) + 1);
    add_delete();
  }
  
  function add_more() {
    $('.add_more').click(function() {
      const prefix = $(this).siblings('div').attr('id').split('-')[0];
      add_form(prefix);
    });
  }
  
  function add_delete() {
    $('.delete-form').click(function() {
      const prefix = $(this).closest('div').attr('id');
      $(`#id_${prefix}-DELETE`).prop('checked', true);
      $(`#${prefix}`).css('display', 'none');
    });
  }
  