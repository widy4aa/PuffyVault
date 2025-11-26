<?php
/**
 * Router Class
 * Handles URL routing and dispatching to controllers
 */

class Router {
    private $routes = [];
    private $notFoundCallback;
    
    /**
     * Add a GET route
     */
    public function get($path, $callback) {
        $this->addRoute('GET', $path, $callback);
    }
    
    /**
     * Add a POST route
     */
    public function post($path, $callback) {
        $this->addRoute('POST', $path, $callback);
    }
    
    /**
     * Add a route for any HTTP method
     */
    private function addRoute($method, $path, $callback) {
        $this->routes[] = [
            'method' => $method,
            'path' => $path,
            'callback' => $callback
        ];
    }
    
    /**
     * Set 404 handler
     */
    public function notFound($callback) {
        $this->notFoundCallback = $callback;
    }
    
    /**
     * Dispatch the request
     */
    public function dispatch() {
        $method = $_SERVER['REQUEST_METHOD'];
        $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
        
        // Remove base path if exists
        $basePath = parse_url(BASE_URL, PHP_URL_PATH) ?? '';
        if ($basePath && strpos($path, $basePath) === 0) {
            $path = substr($path, strlen($basePath));
        }
        
        // Ensure path starts with /
        if ($path === '' || $path[0] !== '/') {
            $path = '/' . $path;
        }
        
        foreach ($this->routes as $route) {
            if ($route['method'] !== $method) {
                continue;
            }
            
            $pattern = $this->convertToRegex($route['path']);
            if (preg_match($pattern, $path, $matches)) {
                array_shift($matches); // Remove full match
                return $this->invokeCallback($route['callback'], $matches);
            }
        }
        
        // No route found
        if ($this->notFoundCallback) {
            return call_user_func($this->notFoundCallback);
        }
        
        http_response_code(404);
        echo "404 - Page Not Found";
    }
    
    /**
     * Convert route path to regex pattern
     */
    private function convertToRegex($path) {
        // Replace :param with regex capture group
        $pattern = preg_replace('/\/:([^\/]+)/', '/([^/]+)', $path);
        return '#^' . $pattern . '$#';
    }
    
    /**
     * Invoke the callback function
     */
    private function invokeCallback($callback, $params = []) {
        if (is_callable($callback)) {
            return call_user_func_array($callback, $params);
        }
        
        if (is_string($callback)) {
            list($controller, $method) = explode('@', $callback);
            
            $controllerFile = CONTROLLER_PATH . '/' . $controller . '.php';
            if (!file_exists($controllerFile)) {
                throw new Exception("Controller file not found: $controllerFile");
            }
            
            require_once $controllerFile;
            
            if (!class_exists($controller)) {
                throw new Exception("Controller class not found: $controller");
            }
            
            $controllerInstance = new $controller();
            
            if (!method_exists($controllerInstance, $method)) {
                throw new Exception("Method $method not found in controller $controller");
            }
            
            return call_user_func_array([$controllerInstance, $method], $params);
        }
    }
    
    /**
     * Redirect to a path
     */
    public static function redirect($path) {
        header('Location: ' . BASE_URL . $path);
        exit;
    }
}
