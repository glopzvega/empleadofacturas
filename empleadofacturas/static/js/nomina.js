function _format_moneda(value)
{
    value = value.toLocaleString('es-MX', { style: 'currency', currency: 'MXN' })
    return value;
}

function actualizar_total()
{
    let pago = $("#id_monto_pago").attr("pago");
    let tipo =  $("#id_tipo").attr("tipo");
    let total = 0;
    if (tipo == "salario")    
    {
        let dias = $("#id_dias_trabajados").val();
        total = dias * pago;
    }
    else
    {
        let horas = $("#id_horas_trabajadas").val();
        total = horas * pago;
    }

    $(".total").html(_format_moneda(total));
}

function guardar_nomina()
{
    if($("#id_horas_trabajadas").val() == 0 && $("#id_dias_trabajados").val() == 0)
    {
        alert("El total de la nómina debe ser mayor a 0");
        return false;
    }
    data = {
        "empleado" : $("#id_empleado").val(),
        "tipo" : $("#id_tipo").attr("tipo"),
        "horas_trabajadas" : $("#id_horas_trabajadas").val(),
        "dias_trabajados" : $("#id_dias_trabajados").val()
    }
    params = {"data" : JSON.stringify(data), "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val()}
    $.post("/nomina/", params, function(res){
        console.log(res)
        if(res.success)
        {
            alert("Se ha guardado correctamente.");
            location.href = "/nominas"
        }
        else
        {
            alert("Ocurrio un problema al guardar la factura, verifique los datos.")
        }
    }, "json")
}

$("#guardar_nomina").on("click", function(e){
    e.preventDefault();
    guardar_nomina();
})

function obtener_empleado(id_empleado)
{
    $.getJSON(`/nomina/empleado/${id_empleado}/`, function(res){
        console.log(res);
        if(res.success)
        {
            if(res.data.tipo == "salario")
            {
                $("#id_tipo").attr("tipo", res.data.tipo).val("Asalariado");
                $("#id_monto_pago").attr("pago", res.data.pago_dia).val(_format_moneda(res.data.pago_dia));
                $("#id_dias_trabajados").prop("readonly", false);
                $("#id_horas_trabajadas").prop("readonly", true);
            }
            else
            {
                $("#id_tipo").attr("tipo", res.data.tipo).val("Pago por hora");
                $("#id_monto_pago").attr("pago", res.data.pago_hora).val(_format_moneda(res.data.pago_hora));
                $("#id_dias_trabajados").prop("readonly", true);
                $("#id_horas_trabajadas").prop("readonly", false);
            }
        }
    });
}

$("#id_empleado").on("change", function(){
    let id = $(this).val()
    if (id != "")
    {
        $("#guardar_nomina").removeClass("disabled").prop("disabled", false);
        obtener_empleado(id)
    }
    else
    {
        $("#id_tipo").val("");
        $("#id_monto_pago").val("");
        $("#id_dias_trabajados").val("").prop("readonly", true);
        $("#id_horas_trabajadas").val("").prop("readonly", true);
        $("#guardar_nomina").addClass("disabled").prop("disabled", true);
    }
});

$("#id_dias_trabajados").on("change", function(){
    actualizar_total();
})

$("#id_horas_trabajadas").on("change", function(){
    actualizar_total();
})