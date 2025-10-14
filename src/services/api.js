/**
 * API Client for Exam Seat Allocator Backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      // Handle different response types
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else if (contentType && contentType.includes('application/pdf')) {
        // Handle PDF downloads
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        
        // Extract filename from response headers or use default
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'allocation_report.pdf';
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
          if (filenameMatch && filenameMatch[1]) {
            filename = filenameMatch[1].replace(/['"]/g, '');
          }
        }
        
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        return { success: true, filename };
      }

      return await response.text();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Student endpoints
  async getStudents() {
    return this.request('/students');
  }

  async createStudent(studentData) {
    return this.request('/students', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
  }

  async updateStudent(studentId, studentData) {
    return this.request(`/students/${studentId}`, {
      method: 'PUT',
      body: JSON.stringify(studentData),
    });
  }

  async deleteStudent(studentId) {
    return this.request(`/students/${studentId}`, {
      method: 'DELETE',
    });
  }

  async getSubjectsFromStudents() {
    return this.request('/students/subjects');
  }

  // Room endpoints
  async getRooms() {
    return this.request('/rooms');
  }

  async createRoom(roomData) {
    return this.request('/rooms', {
      method: 'POST',
      body: JSON.stringify(roomData),
    });
  }

  async updateRoom(roomId, roomData) {
    return this.request(`/rooms/${roomId}`, {
      method: 'PUT',
      body: JSON.stringify(roomData),
    });
  }

  async deleteRoom(roomId) {
    return this.request(`/rooms/${roomId}`, {
      method: 'DELETE',
    });
  }

  // Subject endpoints
  async getSubjects() {
    return this.request('/subjects');
  }

  async getSubjectNames() {
    return this.request('/subjects/names');
  }

  async createSubject(subjectName) {
    return this.request('/subjects', {
      method: 'POST',
      body: JSON.stringify({ name: subjectName }),
    });
  }

  async deleteSubjectByName(subjectName) {
    return this.request(`/subjects/${encodeURIComponent(subjectName)}`, {
      method: 'DELETE',
    });
  }

  // Allocation endpoints
  async getAllocations() {
    return this.request('/allocations');
  }

  async createAllocation(strategy = 'mixed', subjectFilter = '') {
    return this.request('/allocations', {
      method: 'POST',
      body: JSON.stringify({
        strategy,
        subject_filter: subjectFilter,
      }),
    });
  }

  async getAllocation(allocationId) {
    return this.request(`/allocations/${allocationId}`);
  }

  async getLatestAllocation() {
    return this.request('/allocations/latest');
  }

  async generateReport(allocationId) {
    return this.request(`/allocations/${allocationId}/report`);
  }

  async deleteAllocation(allocationId) {
    return this.request(`/allocations/${allocationId}`, {
      method: 'DELETE',
    });
  }
}

export default new ApiClient();