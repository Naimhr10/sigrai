<?php
$conexion = new mysqli("localhost", "root", "", "ia_medica");
if ($conexion->connect_error) {
    die("Error de conexión: " . $conexion->connect_error);
}
?>