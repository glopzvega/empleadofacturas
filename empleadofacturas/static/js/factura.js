var productos = [];

$.getJSON("/factura/productos", function(res){
    console.log(res)
    if(res.success && res.data.length > 0)
    {
        productos = res.data;
    }
});

function _get_productos_opts(productos)
{
    console.log(productos)
    let options = "<option value=''>Seleccione un producto</option>"
    productos.forEach(function(value, index){
        options += "<option value='"+value.id+"'>"+value.nombre+"</option>"
    });
    return options;
}

function _get_producto(id_producto)
{
    if (id_producto != "")
    {        
        let producto = false;
        productos.forEach(function(value, index){
            if (value.id == id_producto)
            {
                producto = value;
                return false;
            }
        });
        if (producto)
            return producto;
    }
    return false;
}

function _get_precio(id_producto)
{
    let precio = 0;
    let producto = _get_producto(id_producto);
    if (producto)
    {
        precio = producto.precio;
    }
    // precio = precio.toLocaleString('es-MX', { style: 'currency', currency: 'MXN' })
    return precio;
}

function _get_monto(row)
{
    // debugger
    let monto = 0;
    let precio = parseFloat(row.find(".precio").val());
    let cantidad = parseFloat(row.find(".cantidad").val());    
    monto = precio * cantidad;
    return {"monto" : monto};    
}

function _get_descuento(row)
{
    // debugger
    let data = _get_monto(row);
    let monto = data["monto"];
    let descuento = parseFloat(row.find(".descuento").val());
    descuento = monto * (descuento / 100);
    data["descuento"] = descuento;
    return data;
}

function _get_base_impuesto(row)
{
    let data = _get_descuento(row);    
    let monto = data["monto"];
    let descuento = data["descuento"];
    let base = monto - descuento;
    // debugger
    data["base"] = base;
    return data;
}

function _get_impuesto(row)
{
    let data = _get_base_impuesto(row); 
    let base = data["base"];
    // debugger  
    let impuesto = parseFloat(row.find(".impuesto").val());
    impuesto = base * (impuesto / 100);
    data["impuesto"] = impuesto;
    return data;
}

function _get_subtotal(row)
{    
    let data = _get_impuesto(row);
    let base = data["base"];
    let impuesto = data["impuesto"];
    let subtotal = base + impuesto; 
    // debugger   
    data["subtotal"] = subtotal;
    return data;
}

function _format_moneda(value)
{
    value = value.toLocaleString('es-MX', { style: 'currency', currency: 'MXN' })
    return value;
}

function _get_datos_generales()
{
    // debugger
  let total = 0;
  let subtotal = 0;
  let descuento = 0;
  let impuesto = 0;
  $("#tabla_productos tbody > tr").each(function(index, row){
    row = $(row);
    data = _get_subtotal(row);
    subtotal += data["monto"];
    descuento += data["descuento"];
    impuesto += data["impuesto"];
    total += data["subtotal"];
  });
  $("#totales").find(".subtotal").html(_format_moneda(subtotal));
  $("#totales").find(".descuento").html(_format_moneda(descuento));
  $("#totales").find(".impuesto").html(_format_moneda(impuesto));
  $("#totales").find(".total").html(_format_moneda(total));
}

$("#add_producto").on("click", function(e){
    e.preventDefault();    
    $("#tabla_productos").append(
        `<tr>
            <td>
                <select class='producto form-control'>
                    ${_get_productos_opts(productos)}
                </select>
            </td>
            <td>
                <input type="number" min="0" value="0" step=".01" class="precio form-control">
            </td>
            <td>
                <input type="number" min="0" value="1" class="cantidad form-control">
            </td>
            <td>
                <input type="number" min="0" max="100" value="16" class="impuesto form-control">
            </td>
            <td>
                <input type="number" min="0" max="100" value="0" class="descuento form-control">
            </td>
            <td>
                <strong class="subtotal">$0.00</strong>
            </td>
            <td>
                <a class="quitar btn btn-danger">X</a>
            </td>
         </tr>`
    );
    eventos();
})

function eventos(){
    
    $("#tabla_productos tr").find(".quitar").off("click").on("click", function(){
        let field = $(this);
        let fila = field.parents("tr"); 
        fila.remove();
        _get_datos_generales();      
    });

    $("#tabla_productos tr").find(".precio,.cantidad,.impuesto,.descuento").off("change").on("change", function(){
        let field = $(this);
        let fila = field.parents("tr");        
        let data = _get_subtotal(fila);
        let subtotal = data["subtotal"];
        fila.find(".subtotal").html(_format_moneda(subtotal));
        _get_datos_generales();
    });
    
    $("#tabla_productos tr").find(".producto").off("change").on("change", function(){
        let select = $(this);
        let fila = select.parents("tr");
        let id_producto = select.val();
        let precio = _get_precio(id_producto);
        fila.find(".precio").val(precio).change();  
    });
}

eventos();

function _get_lineas_factura()
{
    lineas = [];
    $("#tabla_productos tbody > tr").each(function(index, value){
        let row = $(value);
        linea = {
            "producto" : parseFloat(row.find(".producto").val()),
            "precio" : parseFloat(row.find(".precio").val()),
            "cantidad" : parseFloat(row.find(".cantidad").val()),
            "impuesto" : parseFloat(row.find(".impuesto").val()),
            "descuento" : parseFloat(row.find(".descuento").val())
        }
        lineas.push(linea);
    })
    return lineas;
}

function _guardar_factura()
{
    data = {
        "cliente" :parseFloat($("#id_cliente").val()),
        "fecha" : $("#id_fecha").val(),
        "lineas" : _get_lineas_factura()        
    }
    params = {"data" : JSON.stringify(data), "csrfmiddlewaretoken" : $("[name='csrfmiddlewaretoken']").val()}
    $.post("/factura/", params, function(res){
        console.log(res)
        if(res.success)
        {
            alert("Se ha guardado correctamente.");
            location.href = "/facturas"
        }
        else
        {
            alert("Ocurrio un problema al guardar la factura, verifique los datos.")
        }
    }, "json")
}

$("#factura").on("submit", function(e){
    e.preventDefault();
    let id_cliente = $("#id_cliente").val()
    if (id_cliente == "")
    {
        alert("Debe seleccionar un cliente"); 
        $("#id_cliente").focus();  
        return false
    }
    let productos = $("#tabla_productos tbody > tr").length;
    if (productos == 0)
    {
        alert("Debe agregar un producto"); 
        $("#add_producto").click();
        return false
    }
    _guardar_factura()
})