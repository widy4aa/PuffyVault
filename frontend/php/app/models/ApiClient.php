<?php
/**
 * API Client
 * Base class for API communication with Flask backend
 */

class ApiClient {
    protected $baseUrl;
    protected $timeout;
    
    public function __construct() {
        $this->baseUrl = API_BASE_URL;
        $this->timeout = API_TIMEOUT;
    }
    
    /**
     * Make HTTP request to API
     */
    protected function request($endpoint, $method = 'GET', $data = null, $headers = []) {
        $url = $this->baseUrl . $endpoint;
        
        $ch = curl_init();
        
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, $this->timeout);
        
        // Set method
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        
        // Set headers
        $defaultHeaders = [
            'Content-Type: application/json',
            'Accept: application/json'
        ];
        
        $allHeaders = array_merge($defaultHeaders, $headers);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $allHeaders);
        
        // Set body for POST/PUT
        if ($data !== null && in_array($method, ['POST', 'PUT', 'PATCH'])) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        
        curl_close($ch);
        
        if ($error) {
            throw new Exception("API request failed: $error");
        }
        
        $responseData = json_decode($response, true);
        
        if ($httpCode >= 400) {
            $message = $responseData['message'] ?? $responseData['error'] ?? 'Unknown error';
            throw new Exception($message);
        }
        
        return $responseData;
    }
    
    /**
     * GET request
     */
    protected function get($endpoint, $headers = []) {
        return $this->request($endpoint, 'GET', null, $headers);
    }
    
    /**
     * POST request
     */
    protected function post($endpoint, $data, $headers = []) {
        return $this->request($endpoint, 'POST', $data, $headers);
    }
    
    /**
     * PUT request
     */
    protected function put($endpoint, $data, $headers = []) {
        return $this->request($endpoint, 'PUT', $data, $headers);
    }
    
    /**
     * DELETE request
     */
    protected function delete($endpoint, $headers = []) {
        return $this->request($endpoint, 'DELETE', null, $headers);
    }
}
