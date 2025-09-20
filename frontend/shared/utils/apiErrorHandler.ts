// Utility functions for API error handling
export const handleApiError = (error: any): string => {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return '网络连接失败，请确保后端服务正在运行';
  }
  
  if (error.message) {
    return error.message;
  }
  
  return '未知错误';
};

export const fetchWithAuth = async (
  url: string,
  token: string,
  options: RequestInit = {}
): Promise<Response> => {
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  return fetch(url, config);
};

export const fetchWithAdminAuth = async (
  url: string,
  token: string,
  options: RequestInit = {}
): Promise<Response> => {
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  return fetch(url, config);
};