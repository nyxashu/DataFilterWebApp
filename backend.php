<?php
header('Content-Type: application/json');

// Database connection parameters
$servername = "localhost"; // Use "localhost" if the script and MySQL are on the same server
$username = "u924372753_xlsx";
$password = "Market@2023";
$dbname = "u924372753_database";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    echo json_encode(["error" => "Connection failed: " . $conn->connect_error]);
    exit();
}

// Get query parameters
$job_title = $_GET['job_title'] ?? '';
$industry = $_GET['industry'] ?? '';
$employee_size = $_GET['employee_size'] ?? '';
$country = $_GET['country'] ?? '';

// Prepare SQL query with placeholders
$sql = "SELECT * FROM your_table_name WHERE 1=1";
if (!empty($job_title)) {
    $sql .= " AND JT LIKE ?";
}
if (!empty($industry)) {
    $sql .= " AND Industry LIKE ?";
}
if (!empty($employee_size)) {
    $sql .= " AND EmpSize LIKE ?";
}
if (!empty($country)) {
    $sql .= " AND Country LIKE ?";
}

// Prepare statement
$stmt = $conn->prepare($sql);

// Bind parameters
$params = [];
$types = '';
if (!empty($job_title)) {
    $params[] = "%{$job_title}%";
    $types .= 's';
}
if (!empty($industry)) {
    $params[] = "%{$industry}%";
    $types .= 's';
}
if (!empty($employee_size)) {
    $params[] = "%{$employee_size}%";
    $types .= 's';
}
if (!empty($country)) {
    $params[] = "%{$country}%";
    $types .= 's';
}
if ($params) {
    $stmt->bind_param($types, ...$params);
}

// Execute query
$stmt->execute();

// Get results
$result = $stmt->get_result();

// Fetch data
$data = [];
while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}

// Close connections
$stmt->close();
$conn->close();

// Output data as JSON
echo json_encode($data);
?>
