$(document).ready(function() {
    $code_style = $('#code-style');
    static_css_path = '/static/css/';
    code_styles_path = static_css_path + 'code-style/';

    $('#code-style-select').change(function() {
        val = $(this).val();
        $code_style.attr('href', code_styles_path + val);
    });
});
