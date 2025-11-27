<?php
include("conexion.php");
$resultado = $_POST["resultado"];
$sql = "INSERT INTO resultados (descripcion) VALUES ('$resultado')";
if ($conexion->query($sql) === TRUE) {
    echo "Guardado correctamente";
} else {
    echo "Error: " . $conexion->error;
}
?>