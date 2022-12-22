<?php

// enable error reporting and display errors
error_reporting(E_ALL);
ini_set('display_errors', 1);

// check if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
  // check if a file has been uploaded
  if (isset($_FILES['photo']) && !empty($_FILES['photo']['tmp_name'])) {
    // create a GD image from the uploaded file
    $image = imagecreatefromjpeg($_FILES['photo']['tmp_name']);

    // remove the background from the image
    imagefill($image, 0, 0, imagecolorallocate($image, 255, 255, 255));
    imagecolortransparent($image, imagecolorallocate($image, 255, 255, 255));

    // output the image as a data URI
    header('Content-Type: image/jpeg');
    imagejpeg($image);
  }
}

?>
