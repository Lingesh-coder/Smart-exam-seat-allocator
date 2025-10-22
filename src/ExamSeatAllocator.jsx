import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Users, MapPin, Download, Book, Shuffle, AlertCircle, Upload } from 'lucide-react';
import ApiClient from './services/api';
import CSVUploader from './components/CSVUploader';

const ExamSeatAllocator = () => {
  const [students, setStudents] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [allocations, setAllocations] = useState([]);
  const [currentStudent, setCurrentStudent] = useState({ name: '', roll_number: '', year: '', subjects: [] });
  const [currentRoom, setCurrentRoom] = useState({ name: '', capacity: '' });
  const [currentSubject, setCurrentSubject] = useState('');
  const [allocationStrategy, setAllocationStrategy] = useState('mixed'); // 'mixed', 'separated', or 'optimal_packing'
  const [selectedAllocationSubject, setSelectedAllocationSubject] = useState(''); // For subject-specific allocation
  const [availableSubjects, setAvailableSubjects] = useState([]); // Subjects from students

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showCSVUploaders, setShowCSVUploaders] = useState(false);
  const [availableClasses, setAvailableClasses] = useState([]);
  const [classStatistics, setClassStatistics] = useState({});
  const [showComprehensiveReport, setShowComprehensiveReport] = useState(false);

  // Load data on component mount
  useEffect(() => {
    loadInitialData();
  }, []);

  const showSuccess = (message) => {
    setSuccess(message);
    setError('');
    setTimeout(() => setSuccess(''), 3000);
  };

  const showError = (message) => {
    setError(message);
    setSuccess('');
    setTimeout(() => setError(''), 5000);
  };

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [studentsData, roomsData, subjectsData, availableSubjectsData] = await Promise.all([
        ApiClient.getStudents(),
        ApiClient.getRooms(),
        ApiClient.getSubjectNames(),
        ApiClient.getSubjectsFromStudents()
      ]);
      
      setStudents(studentsData);
      setRooms(roomsData);
      setSubjects(subjectsData);
      setAvailableSubjects(availableSubjectsData);
      
      // Load available classes if there's an existing allocation
      await loadAvailableClasses();
    } catch (err) {
      showError('Failed to load data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Add subject
  const addSubject = async () => {
    if (!currentSubject || subjects.includes(currentSubject)) {
      return;
    }

    setLoading(true);
    try {
      await ApiClient.createSubject(currentSubject);
      setSubjects([...subjects, currentSubject]);
      setCurrentSubject('');
      showSuccess('Subject added successfully');
    } catch (err) {
      showError('Failed to add subject: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Add student
  const addStudent = async () => {
    if (!currentStudent.name || !currentStudent.roll_number || !currentStudent.year || !currentStudent.subjects || currentStudent.subjects.length === 0) {
      showError('Please fill all student fields and select at least one subject');
      return;
    }

    setLoading(true);
    try {
      await ApiClient.createStudent({
        name: currentStudent.name,
        roll_number: currentStudent.roll_number,
        year: currentStudent.year,
        subjects: currentStudent.subjects
      });
      
      // Reload students and available subjects
      const [studentsData, availableSubjectsData] = await Promise.all([
        ApiClient.getStudents(),
        ApiClient.getSubjectsFromStudents()
      ]);
      setStudents(studentsData);
      setAvailableSubjects(availableSubjectsData);
      setCurrentStudent({ name: '', roll_number: '', year: '', subjects: [] });
      showSuccess('Student added successfully');
    } catch (err) {
      showError('Failed to add student: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Add room
  const addRoom = async () => {
    if (!currentRoom.name || !currentRoom.capacity) {
      showError('Please fill all room fields');
      return;
    }

    const capacity = parseInt(currentRoom.capacity);
    if (capacity <= 0) {
      showError('Room capacity must be greater than 0');
      return;
    }

    if (capacity > 50) {
      showError('Room capacity cannot exceed 50 seats');
      return;
    }

    setLoading(true);
    try {
      await ApiClient.createRoom({
        name: currentRoom.name,
        capacity: capacity
      });
      
      // Reload rooms
      const roomsData = await ApiClient.getRooms();
      setRooms(roomsData);
      setCurrentRoom({ name: '', capacity: '' });
      showSuccess('Room added successfully');
    } catch (err) {
      showError('Failed to add room: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Remove functions
  const removeStudent = async (id) => {
    setLoading(true);
    try {
      await ApiClient.deleteStudent(id);
      setStudents(students.filter(student => student._id !== id));
      showSuccess('Student removed successfully');
    } catch (err) {
      showError('Failed to remove student: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const removeRoom = async (id) => {
    setLoading(true);
    try {
      await ApiClient.deleteRoom(id);
      setRooms(rooms.filter(room => room._id !== id));
      showSuccess('Room removed successfully');
    } catch (err) {
      showError('Failed to remove room: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const removeSubject = async (subject) => {
    setLoading(true);
    try {
      await ApiClient.deleteSubjectByName(subject);
      setSubjects(subjects.filter(s => s !== subject));
      // Reload students since they may have been deleted
      const studentsData = await ApiClient.getStudents();
      setStudents(studentsData);
      showSuccess('Subject and associated students removed successfully');
    } catch (err) {
      showError('Failed to remove subject: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Bulk deletion methods
  const deleteAllStudents = async () => {
    if (students.length === 0) {
      showError('No students to delete');
      return;
    }

    if (!window.confirm(`Are you sure you want to delete all ${students.length} students? This action cannot be undone.`)) {
      return;
    }

    setLoading(true);
    try {
      const result = await ApiClient.deleteAllStudents();
      setStudents([]);
      setAvailableSubjects([]);
      setAllocations([]); // Clear allocations since students are gone
      showSuccess(`Successfully deleted ${result.deleted_count} students`);
    } catch (err) {
      showError('Failed to delete all students: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteAllRooms = async () => {
    if (rooms.length === 0) {
      showError('No rooms to delete');
      return;
    }

    if (!window.confirm(`Are you sure you want to delete all ${rooms.length} rooms? This action cannot be undone.`)) {
      return;
    }

    setLoading(true);
    try {
      const result = await ApiClient.deleteAllRooms();
      setRooms([]);
      setAllocations([]); // Clear allocations since rooms are gone
      showSuccess(`Successfully deleted ${result.deleted_count} rooms`);
    } catch (err) {
      showError('Failed to delete all rooms: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteAllSubjects = async () => {
    if (subjects.length === 0) {
      showError('No subjects to delete');
      return;
    }

    if (!window.confirm(`Are you sure you want to delete all ${subjects.length} subjects? This will also delete all associated students. This action cannot be undone.`)) {
      return;
    }

    setLoading(true);
    try {
      const result = await ApiClient.deleteAllSubjects();
      setSubjects([]);
      setAvailableSubjects([]);
      // Reload students since they may have been deleted
      const studentsData = await ApiClient.getStudents();
      setStudents(studentsData);
      setAllocations([]); // Clear allocations
      showSuccess(`Successfully deleted ${result.deleted_count} subjects and associated students`);
    } catch (err) {
      showError('Failed to delete all subjects: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteAllAllocations = async () => {
    if (allocations.length === 0) {
      showError('No allocations to delete');
      return;
    }

    if (!window.confirm('Are you sure you want to delete all allocations? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    try {
      const result = await ApiClient.deleteAllAllocations();
      setAllocations([]);
      setAvailableClasses([]);
      setClassStatistics({});
      showSuccess(`Successfully deleted ${result.deleted_count} allocations`);
    } catch (err) {
      showError('Failed to delete all allocations: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Advanced seat allocation with subject separation
  const allocateSeats = async () => {
    if (students.length === 0 || rooms.length === 0) {
      showError('Please add students and rooms first');
      return;
    }

    // Check capacity for the specific subject or all students
    let studentsToAllocate = students;
    if (selectedAllocationSubject) {
      studentsToAllocate = students.filter(student => {
        const studentSubjects = student.subjects || [student.subject];
        return studentSubjects.includes(selectedAllocationSubject);
      });
      
      if (studentsToAllocate.length === 0) {
        showError(`No students found for subject: ${selectedAllocationSubject}`);
        return;
      }
    }

    const totalCapacity = rooms.reduce((sum, room) => sum + room.capacity, 0);
    if (studentsToAllocate.length > totalCapacity) {
      showError('Not enough room capacity for selected students');
      return;
    }

    setLoading(true);
    try {
      const result = await ApiClient.createAllocation(allocationStrategy, selectedAllocationSubject);
      setAllocations(result.allocation.allocations);

      await loadAvailableClasses();
      
      const message = selectedAllocationSubject 
        ? `Seats allocated successfully for ${selectedAllocationSubject}`
        : 'Seats allocated successfully';
      showSuccess(message);
    } catch (err) {
      showError('Failed to allocate seats: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Generate allocation report
  const generateReport = async () => {
    if (allocations.length === 0) {
      showError('Please allocate seats first');
      return;
    }

    setLoading(true);
    try {
      const latestAllocation = await ApiClient.getLatestAllocation();
      if (!latestAllocation) {
        showError('No allocation found');
        return;
      }

      const result = await ApiClient.generateReport(latestAllocation._id);
      showSuccess(`PDF report (${result.filename}) downloaded successfully`);
    } catch (err) {
      showError('Failed to generate PDF report: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load available classes from current allocation
  const loadAvailableClasses = async () => {
    try {
      const latestAllocation = await ApiClient.getLatestAllocation();
      if (latestAllocation) {
        const classData = await ApiClient.getAllocationClasses(latestAllocation._id);
        setAvailableClasses(classData.classes);
        setClassStatistics(classData.class_statistics);
      }
    } catch (err) {
      console.error('Failed to load available classes:', err);
    }
  };

  // Generate class-specific report
  const generateClassReport = async (classYear) => {
    setLoading(true);
    try {
      const latestAllocation = await ApiClient.getLatestAllocation();
      if (!latestAllocation) {
        showError('No allocation found');
        return;
      }

      const result = await ApiClient.generateClassReport(latestAllocation._id, classYear);
      showSuccess(`Class ${classYear} PDF report (${result.filename}) downloaded successfully`);
    } catch (err) {
      showError(`Failed to generate Class ${classYear} PDF report: ` + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Calculate comprehensive report data
  const getComprehensiveReport = () => {
    if (allocations.length === 0) return null;

    const totalStudentsAllocated = allocations.reduce((sum, allocation) => sum + allocation.students.length, 0);
    const totalRoomsUsed = allocations.length;
    const totalCapacity = rooms.reduce((sum, room) => sum + room.capacity, 0);
    const totalEmptySeats = totalCapacity - totalStudentsAllocated;

    // Subject distribution across all rooms
    const subjectDistribution = {};
    allocations.forEach(allocation => {
      Object.entries(allocation.subject_breakdown || {}).forEach(([subject, count]) => {
        subjectDistribution[subject] = (subjectDistribution[subject] || 0) + count;
      });
    });

    // Year/Class distribution
    const yearDistribution = {};
    allocations.forEach(allocation => {
      allocation.students.forEach(studentAlloc => {
        const year = studentAlloc.student.year;
        yearDistribution[year] = (yearDistribution[year] || 0) + 1;
      });
    });

    // Room utilization statistics
    const roomStats = allocations.map(allocation => ({
      roomName: allocation.room.name,
      capacity: allocation.room.capacity,
      allocated: allocation.students.length,
      utilization: Math.round((allocation.students.length / allocation.room.capacity) * 100),
      subjects: Object.keys(allocation.subject_breakdown || {}).length,
      subjectBreakdown: allocation.subject_breakdown || {}
    }));

    // Overall statistics
    const allocationRate = totalCapacity > 0 ? Math.round((totalStudentsAllocated / totalCapacity) * 100) : 0;
    const avgRoomUtilization = roomStats.length > 0 ? Math.round(roomStats.reduce((sum, room) => sum + room.utilization, 0) / roomStats.length) : 0;
    
    // Packing efficiency metrics
    const usedCapacity = allocations.reduce((sum, allocation) => sum + allocation.room.capacity, 0);
    const packingEfficiency = usedCapacity > 0 ? Math.round((totalStudentsAllocated / usedCapacity) * 100) : 0;
    const roomsSaved = rooms.length - totalRoomsUsed;
    const capacitySaved = totalCapacity - usedCapacity;

    return {
      overview: {
        totalStudentsAllocated,
        totalStudentsInSystem: students.length,
        totalRoomsUsed,
        totalRoomsInSystem: rooms.length,
        totalCapacity,
        totalEmptySeats,
        allocationRate,
        avgRoomUtilization,
        packingEfficiency,
        roomsSaved,
        capacitySaved,
        usedCapacity
      },
      subjectDistribution,
      yearDistribution,
      roomStats,
      detailedAllocations: allocations
    };
  };

  // CSV Upload Functions
  const handleStudentsCSVUpload = async (csvContent) => {
    const result = await ApiClient.uploadStudentsCSV(csvContent);
    // Reload data after successful upload
    const [studentsData, availableSubjectsData] = await Promise.all([
      ApiClient.getStudents(),
      ApiClient.getSubjectsFromStudents()
    ]);
    setStudents(studentsData);
    setAvailableSubjects(availableSubjectsData);
    return result;
  };

  const handleRoomsCSVUpload = async (csvContent) => {
    const result = await ApiClient.uploadRoomsCSV(csvContent);
    // Reload data after successful upload
    const roomsData = await ApiClient.getRooms();
    setRooms(roomsData);
    return result;
  };

  const handleSubjectsCSVUpload = async (csvContent) => {
    const result = await ApiClient.uploadSubjectsCSV(csvContent);
    // Reload data after successful upload
    const subjectsData = await ApiClient.getSubjectNames();
    setSubjects(subjectsData);
    return result;
  };

  const handleDownloadStudentsSample = async () => {
    const result = await ApiClient.getStudentsCSVSample();
    downloadCSVSample(result.sample_csv, 'students_sample.csv');
  };

  const handleDownloadRoomsSample = async () => {
    const result = await ApiClient.getRoomsCSVSample();
    downloadCSVSample(result.sample_csv, 'rooms_sample.csv');
  };

  const handleDownloadSubjectsSample = async () => {
    const result = await ApiClient.getSubjectsCSVSample();
    downloadCSVSample(result.sample_csv, 'subjects_sample.csv');
  };

  const downloadCSVSample = (csvContent, filename) => {
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  return (
    <div className="max-w-7xl mx-auto p-6 bg-slate-100 min-h-screen">
      {/* Status Messages */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border-2 border-red-500 text-red-800 rounded-lg flex items-center font-medium">
          <AlertCircle size={20} className="mr-2 text-red-600" />
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-4 bg-green-50 border-2 border-green-500 text-green-800 rounded-lg flex items-center font-medium">
          <AlertCircle size={20} className="mr-2 text-green-600" />
          {success}
        </div>
      )}

      <div className="bg-white rounded-lg shadow-xl p-6 mb-6 border border-gray-200">
        <h1 className="text-3xl font-bold text-center text-blue-700 mb-2">
          IT Department Exam Seat Allocator
        </h1>
        <p className="text-center text-gray-700 font-medium">
          Anti-copying seat allocation with subject separation
        </p>
        {loading && (
          <div className="text-center mt-2">
            <span className="text-blue-700 font-semibold">Loading...</span>
          </div>
        )}
      </div>

      {/* CSV Import Section */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6 border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold flex items-center text-gray-800">
              <Upload className="mr-2 text-indigo-600" size={20} />
              Bulk Import from CSV
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              Import students, rooms, and subjects from CSV files
            </p>
          </div>
          <button
            onClick={() => setShowCSVUploaders(!showCSVUploaders)}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            disabled={loading}
          >
            {showCSVUploaders ? 'Hide' : 'Show'} CSV Import
          </button>
        </div>

        {showCSVUploaders && (
          <div className="space-y-6">
            <CSVUploader
              title="Import Students"
              description="Upload student data with their subjects"
              sampleColumns="name, roll_number, year, subjects (comma-separated)"
              onUpload={handleStudentsCSVUpload}
              onDownloadSample={handleDownloadStudentsSample}
              loading={loading}
            />
            
            <CSVUploader
              title="Import Rooms"
              description="Upload room data with capacities"
              sampleColumns="name, capacity"
              onUpload={handleRoomsCSVUpload}
              onDownloadSample={handleDownloadRoomsSample}
              loading={loading}
            />
            
            <CSVUploader
              title="Import Subjects"
              description="Upload subject codes/names"
              sampleColumns="name"
              onUpload={handleSubjectsCSVUpload}
              onDownloadSample={handleDownloadSubjectsSample}
              loading={loading}
            />
          </div>
        )}
      </div>

      {/* Data Management - Bulk Deletion */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6 border border-red-200">
        <h2 className="text-xl font-bold mb-4 flex items-center text-gray-800">
          <Trash2 className="mr-2 text-red-600" size={20} />
          Data Management - Bulk Delete
        </h2>
        <p className="text-sm text-gray-600 mb-4">
          Clear all data to start fresh. Use with caution - these actions cannot be undone.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={deleteAllStudents}
            disabled={loading || students.length === 0}
            className="bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 flex items-center justify-center disabled:opacity-50 font-medium shadow-md transition-colors"
          >
            <Trash2 size={16} className="mr-2" />
            Delete All Students ({students.length})
          </button>
          
          <button
            onClick={deleteAllRooms}
            disabled={loading || rooms.length === 0}
            className="bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 flex items-center justify-center disabled:opacity-50 font-medium shadow-md transition-colors"
          >
            <Trash2 size={16} className="mr-2" />
            Delete All Rooms ({rooms.length})
          </button>
          
          <button
            onClick={deleteAllSubjects}
            disabled={loading || subjects.length === 0}
            className="bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 flex items-center justify-center disabled:opacity-50 font-medium shadow-md transition-colors"
          >
            <Trash2 size={16} className="mr-2" />
            Delete All Subjects ({subjects.length})
          </button>
          
          <button
            onClick={deleteAllAllocations}
            disabled={loading || allocations.length === 0}
            className="bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 flex items-center justify-center disabled:opacity-50 font-medium shadow-md transition-colors"
          >
            <Trash2 size={16} className="mr-2" />
            Delete All Allocations ({allocations.length})
          </button>
        </div>
        
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-300 rounded-lg">
          <p className="text-sm text-yellow-800 font-medium">
            ⚠️ Warning: Deleting subjects will also delete all associated students. 
            Deleting students or rooms will clear all allocations.
          </p>
        </div>
      </div>

      {/* Subject Management */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6 border border-gray-200">
        <h2 className="text-xl font-bold mb-4 flex items-center text-gray-800">
          <Book className="mr-2 text-blue-600" size={20} />
          Subject Management
        </h2>
        
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            placeholder="Subject Code (e.g., CS301, IT205)"
            value={currentSubject}
            onChange={(e) => setCurrentSubject(e.target.value)}
            className="flex-1 p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
            disabled={loading}
          />
          <button
            onClick={addSubject}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 flex items-center disabled:opacity-50 font-medium shadow-md transition-colors"
          >
            <Plus size={16} className="mr-1" />
            Add
          </button>
        </div>

        <div className="flex flex-wrap gap-2">
          {subjects.map(subject => (
            <div key={subject} className="flex items-center bg-blue-50 border-2 border-blue-200 text-blue-900 px-4 py-2 rounded-lg text-sm font-medium">
              <span>{subject}</span>
              <button
                onClick={() => removeSubject(subject)}
                disabled={loading}
                className="ml-2 text-red-600 hover:text-red-800 disabled:opacity-50 p-1 rounded hover:bg-red-50"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Student Management */}
        <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
          <h2 className="text-xl font-bold mb-4 flex items-center text-gray-800">
            <Users className="mr-2 text-green-600" size={20} />
            Student Management
          </h2>
          
          <div className="space-y-3 mb-4">
            <input
              type="text"
              placeholder="Student Name"
              value={currentStudent.name}
              onChange={(e) => setCurrentStudent({...currentStudent, name: e.target.value})}
              className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
              disabled={loading}
            />
            <input
              type="text"
              placeholder="Roll Number"
              value={currentStudent.roll_number}
              onChange={(e) => setCurrentStudent({...currentStudent, roll_number: e.target.value})}
              className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
              disabled={loading}
            />
            <select
              value={currentStudent.year}
              onChange={(e) => setCurrentStudent({...currentStudent, year: e.target.value})}
              className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
              disabled={loading}
            >
              <option value="">Select Year</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>
            
            {/* Multi-select for subjects */}
            <div className="space-y-2">
              <label className="text-sm font-bold text-gray-800">Select Subjects (Multiple)</label>
              <div className="border-2 border-gray-300 rounded-lg p-3 max-h-32 overflow-y-auto bg-gray-50">
                {subjects.length === 0 ? (
                  <p className="text-sm text-gray-600 font-medium">Add some subjects first</p>
                ) : (
                  subjects.map(subject => (
                    <label key={subject} className="flex items-center space-x-2 p-2 cursor-pointer hover:bg-blue-50 rounded-lg">
                      <input
                        type="checkbox"
                        checked={currentStudent.subjects.includes(subject)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setCurrentStudent({
                              ...currentStudent,
                              subjects: [...currentStudent.subjects, subject]
                            });
                          } else {
                            setCurrentStudent({
                              ...currentStudent,
                              subjects: currentStudent.subjects.filter(s => s !== subject)
                            });
                          }
                        }}
                        className="rounded text-blue-600 focus:ring-blue-500 w-4 h-4"
                        disabled={loading}
                      />
                      <span className="text-sm font-medium text-gray-800">{subject}</span>
                    </label>
                  ))
                )}
              </div>
              {currentStudent.subjects.length > 0 && (
                <div className="text-sm text-blue-700 font-semibold bg-blue-50 p-2 rounded-lg">
                  Selected: {currentStudent.subjects.join(', ')}
                </div>
              )}
            </div>
            <button
              onClick={addStudent}
              disabled={loading}
              className="w-full bg-green-600 text-white p-3 rounded-lg hover:bg-green-700 flex items-center justify-center disabled:opacity-50 font-medium shadow-md transition-colors"
            >
              <Plus size={16} className="mr-1" />
              Add Student
            </button>
          </div>

          <div className="max-h-40 overflow-y-auto">
            {students.map(student => {
              const studentSubjects = student.subjects || [student.subject];
              return (
                <div key={student._id} className="flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded-lg mb-2">
                  <span className="text-sm">
                    <strong className="text-gray-800">{student.name}</strong> <span className="text-gray-600">({student.roll_number})</span>
                    <br />
                    <span className="text-gray-700 font-medium">
                      Year {student.year} - {studentSubjects.join(', ')}
                    </span>
                  </span>
                  <button
                    onClick={() => removeStudent(student._id)}
                    disabled={loading}
                    className="text-red-600 hover:text-red-800 disabled:opacity-50 p-1 rounded hover:bg-red-50"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              );
            })}
          </div>
          
          <div className="mt-3 text-sm text-gray-800 font-semibold bg-green-50 p-2 rounded-lg">
            Total Students: {students.length}
          </div>
        </div>

        {/* Room Management */}
        <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
          <h2 className="text-xl font-bold mb-4 flex items-center text-gray-800">
            <MapPin className="mr-2 text-purple-600" size={20} />
            Room Management
          </h2>
          
          <div className="space-y-3 mb-4">
            <input
              type="text"
              placeholder="Room Name (e.g., Lab-1, IT-201)"
              value={currentRoom.name}
              onChange={(e) => setCurrentRoom({...currentRoom, name: e.target.value})}
              className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
              disabled={loading}
            />
            <input
              type="number"
              placeholder="Room Capacity (Max: 50)"
              value={currentRoom.capacity}
              onChange={(e) => setCurrentRoom({...currentRoom, capacity: e.target.value})}
              className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
              disabled={loading}
              min="1"
              max="50"
            />
            <button
              onClick={addRoom}
              disabled={loading}
              className="w-full bg-purple-600 text-white p-3 rounded-lg hover:bg-purple-700 flex items-center justify-center disabled:opacity-50 font-medium shadow-md transition-colors"
            >
              <Plus size={16} className="mr-1" />
              Add Room
            </button>
          </div>

          <div className="max-h-40 overflow-y-auto">
            {rooms.map(room => (
              <div key={room._id} className="flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded-lg mb-2">
                <span className="text-sm">
                  <strong className="text-gray-800">{room.name}</strong> <span className="text-gray-600">(Capacity: {room.capacity})</span>
                </span>
                <button
                  onClick={() => removeRoom(room._id)}
                  disabled={loading}
                  className="text-red-600 hover:text-red-800 disabled:opacity-50 p-1 rounded hover:bg-red-50"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
          
          <div className="mt-3 text-sm text-gray-800 font-semibold bg-purple-50 p-2 rounded-lg">
            Total Capacity: {rooms.reduce((sum, room) => sum + room.capacity, 0)}
          </div>
        </div>
      </div>

      {/* Allocation Strategy & Controls */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6 border border-gray-200">
        <div className="mb-6">
          <h3 className="text-lg font-bold mb-4 text-gray-800">Subject Selection</h3>
          <div className="mb-6">
            <label className="block text-sm font-bold text-gray-800 mb-2">
              Select Subject for Allocation (Optional - leave empty for all subjects)
            </label>
            <select
              value={selectedAllocationSubject}
              onChange={(e) => setSelectedAllocationSubject(e.target.value)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
              disabled={loading}
            >
              <option value="">All Subjects</option>
              {availableSubjects.map(subject => (
                <option key={subject} value={subject}>{subject}</option>
              ))}
            </select>
            {selectedAllocationSubject && (
              <p className="text-sm text-blue-700 mt-2 font-semibold bg-blue-50 p-2 rounded-lg">
                Will allocate seats only for students taking: {selectedAllocationSubject}
              </p>
            )}
          </div>
          
          <h3 className="text-lg font-bold mb-3 text-gray-800">Allocation Strategy</h3>
          <div className="flex flex-col gap-3">
            <label className="flex items-start p-3 border-2 border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                name="strategy"
                value="mixed"
                checked={allocationStrategy === 'mixed'}
                onChange={(e) => setAllocationStrategy(e.target.value)}
                className="mr-3 mt-1 w-4 h-4 text-blue-600"
                disabled={loading}
              />
              <span className="text-sm text-gray-800">
                <strong className="text-blue-700">Mixed (Minimize Rooms):</strong> Fill rooms sequentially, separate same subjects within rooms
              </span>
            </label>
            <label className="flex items-start p-3 border-2 border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                name="strategy"
                value="separated"
                checked={allocationStrategy === 'separated'}
                onChange={(e) => setAllocationStrategy(e.target.value)}
                className="mr-3 mt-1 w-4 h-4 text-blue-600"
                disabled={loading}
              />
              <span className="text-sm text-gray-800">
                <strong className="text-green-700">Subject Separated:</strong> Distribute same subjects across different rooms, split large subjects
              </span>
            </label>
            <label className="flex items-start p-3 border-2 border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                name="strategy"
                value="optimal_packing"
                checked={allocationStrategy === 'optimal_packing'}
                onChange={(e) => setAllocationStrategy(e.target.value)}
                className="mr-3 mt-1 w-4 h-4 text-blue-600"
                disabled={loading}
              />
              <span className="text-sm text-gray-800">
                <strong className="text-purple-700">Optimal Packing:</strong> Use minimum rooms possible, shuffle students thoroughly, maximum efficiency
              </span>
            </label>
          </div>
        </div>

        <div className="flex flex-wrap gap-4 justify-center">
          <button
            onClick={allocateSeats}
            disabled={loading || students.length === 0 || rooms.length === 0}
            className="bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700 flex items-center disabled:opacity-50 font-medium shadow-md transition-colors"
          >
            <Shuffle size={18} className="mr-2" />
            Allocate Seats
          </button>
          <button
            onClick={generateReport}
            disabled={loading || allocations.length === 0}
            className="bg-orange-600 text-white px-8 py-3 rounded-lg hover:bg-orange-700 flex items-center disabled:opacity-50 font-medium shadow-md transition-colors"
          >
            <Download size={18} className="mr-2" />
            Download PDF Report
          </button>
        </div>

        {/* Class-specific Reports */}
        {availableClasses.length > 0 && (
          <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
            <h3 className="text-lg font-bold text-green-800 mb-4 flex items-center">
              <Book size={20} className="mr-2" />
              Class-specific Reports
            </h3>
            <p className="text-sm text-gray-700 mb-4">
              Generate PDF reports for individual classes showing only students from that class year.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {availableClasses.map(classYear => (
                <div key={classYear} className="bg-white rounded-lg p-4 border border-green-200 shadow-sm">
                  <div className="text-center mb-3">
                    <div className="text-2xl font-bold text-green-700">
                      {classStatistics[classYear]?.count || 0}
                    </div>
                    <div className="text-xs text-gray-600">
                      Class {classYear} Students
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {classStatistics[classYear]?.rooms?.length || 0} rooms
                    </div>
                  </div>
                  <button
                    onClick={() => generateClassReport(classYear)}
                    disabled={loading}
                    className="w-full bg-green-600 text-white px-3 py-2 rounded-lg hover:bg-green-700 flex items-center justify-center disabled:opacity-50 text-sm font-medium transition-colors"
                  >
                    <Download size={14} className="mr-1" />
                    Class {classYear} PDF
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Comprehensive Report */}
        {allocations.length > 0 && (
          <div className="mt-6 p-6 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg border border-blue-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-blue-800 flex items-center">
                <Book size={20} className="mr-2" />
                Comprehensive Report
              </h3>
              <button
                onClick={() => setShowComprehensiveReport(!showComprehensiveReport)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm font-medium transition-colors"
              >
                {showComprehensiveReport ? 'Hide Details' : 'Show Details'}
              </button>
            </div>
            
            {showComprehensiveReport && (() => {
              const report = getComprehensiveReport();
              if (!report) return null;
              
              return (
                <div className="space-y-6">
                  {/* Overview Statistics */}
                  <div className="bg-white rounded-lg p-6 border border-blue-200">
                    <h4 className="text-lg font-bold text-gray-800 mb-4">Overview Statistics</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center p-3 bg-blue-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-700">{report.overview.totalStudentsAllocated}</div>
                        <div className="text-sm text-gray-600">Students Allocated</div>
                        <div className="text-xs text-gray-500">of {report.overview.totalStudentsInSystem} total</div>
                      </div>
                      <div className="text-center p-3 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-700">{report.overview.totalRoomsUsed}</div>
                        <div className="text-sm text-gray-600">Rooms Used</div>
                        <div className="text-xs text-gray-500">of {report.overview.totalRoomsInSystem} available</div>
                      </div>
                      <div className="text-center p-3 bg-purple-50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-700">{report.overview.allocationRate}%</div>
                        <div className="text-sm text-gray-600">Allocation Rate</div>
                        <div className="text-xs text-gray-500">{report.overview.totalCapacity} total capacity</div>
                      </div>
                      <div className="text-center p-3 bg-orange-50 rounded-lg">
                        <div className="text-2xl font-bold text-orange-700">{report.overview.avgRoomUtilization}%</div>
                        <div className="text-sm text-gray-600">Avg Room Utilization</div>
                        <div className="text-xs text-gray-500">{report.overview.totalEmptySeats} empty seats</div>
                      </div>
                    </div>
                  </div>

                  {/* Packing Efficiency Metrics (shown when rooms are saved) */}
                  {report.overview.roomsSaved > 0 && (
                    <div className="bg-white rounded-lg p-6 border border-green-200">
                      <h4 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                        <span className="text-green-600 mr-2">📦</span>
                        Packing Efficiency
                      </h4>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center p-3 bg-green-50 rounded-lg">
                          <div className="text-2xl font-bold text-green-700">{report.overview.packingEfficiency}%</div>
                          <div className="text-sm text-gray-600">Packing Efficiency</div>
                          <div className="text-xs text-gray-500">{report.overview.usedCapacity} seats used</div>
                        </div>
                        <div className="text-center p-3 bg-emerald-50 rounded-lg">
                          <div className="text-2xl font-bold text-emerald-700">{report.overview.roomsSaved}</div>
                          <div className="text-sm text-gray-600">Rooms Saved</div>
                          <div className="text-xs text-gray-500">optimal packing</div>
                        </div>
                        <div className="text-center p-3 bg-teal-50 rounded-lg">
                          <div className="text-2xl font-bold text-teal-700">{report.overview.capacitySaved}</div>
                          <div className="text-sm text-gray-600">Capacity Saved</div>
                          <div className="text-xs text-gray-500">unused seats</div>
                        </div>
                        <div className="text-center p-3 bg-cyan-50 rounded-lg">
                          <div className="text-2xl font-bold text-cyan-700">
                            {Math.round((report.overview.roomsSaved / report.overview.totalRoomsInSystem) * 100)}%
                          </div>
                          <div className="text-sm text-gray-600">Space Efficiency</div>
                          <div className="text-xs text-gray-500">rooms optimization</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Subject Distribution */}
                  <div className="bg-white rounded-lg p-6 border border-blue-200">
                    <h4 className="text-lg font-bold text-gray-800 mb-4">Subject Distribution</h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                      {Object.entries(report.subjectDistribution)
                        .sort(([,a], [,b]) => b - a)
                        .map(([subject, count]) => (
                          <div key={subject} className="bg-gray-50 p-3 rounded-lg border">
                            <div className="font-bold text-gray-800">{subject}</div>
                            <div className="text-2xl font-bold text-blue-600">{count}</div>
                            <div className="text-xs text-gray-500">
                              {Math.round((count / report.overview.totalStudentsAllocated) * 100)}%
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>

                  {/* Year Distribution */}
                  <div className="bg-white rounded-lg p-6 border border-blue-200">
                    <h4 className="text-lg font-bold text-gray-800 mb-4">Year/Class Distribution</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {Object.entries(report.yearDistribution)
                        .sort(([a], [b]) => parseInt(a) - parseInt(b))
                        .map(([year, count]) => (
                          <div key={year} className="bg-gray-50 p-3 rounded-lg border text-center">
                            <div className="text-sm text-gray-600">Year {year}</div>
                            <div className="text-2xl font-bold text-green-600">{count}</div>
                            <div className="text-xs text-gray-500">
                              {Math.round((count / report.overview.totalStudentsAllocated) * 100)}%
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>

                  {/* Room Statistics */}
                  <div className="bg-white rounded-lg p-6 border border-blue-200">
                    <h4 className="text-lg font-bold text-gray-800 mb-4">Room Utilization Details</h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-gray-200">
                            <th className="text-left py-2 px-3 font-semibold text-gray-700">Room</th>
                            <th className="text-center py-2 px-3 font-semibold text-gray-700">Capacity</th>
                            <th className="text-center py-2 px-3 font-semibold text-gray-700">Allocated</th>
                            <th className="text-center py-2 px-3 font-semibold text-gray-700">Utilization</th>
                            <th className="text-left py-2 px-3 font-semibold text-gray-700">Subjects</th>
                          </tr>
                        </thead>
                        <tbody>
                          {report.roomStats
                            .sort((a, b) => b.utilization - a.utilization)
                            .map((room, index) => (
                              <tr key={room.roomName} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                                <td className="py-2 px-3 font-medium text-gray-800">{room.roomName}</td>
                                <td className="py-2 px-3 text-center">{room.capacity}</td>
                                <td className="py-2 px-3 text-center font-semibold text-blue-600">{room.allocated}</td>
                                <td className="py-2 px-3 text-center">
                                  <span className={`font-semibold ${
                                    room.utilization >= 90 ? 'text-red-600' :
                                    room.utilization >= 70 ? 'text-orange-600' :
                                    room.utilization >= 50 ? 'text-green-600' : 'text-gray-600'
                                  }`}>
                                    {room.utilization}%
                                  </span>
                                </td>
                                <td className="py-2 px-3">
                                  <div className="flex flex-wrap gap-1">
                                    {Object.entries(room.subjectBreakdown).map(([subject, count]) => (
                                      <span key={subject} className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                        {subject}: {count}
                                      </span>
                                    ))}
                                  </div>
                                </td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              );
            })()}
          </div>
        )}
      </div>

      {/* Allocation Results */}
      {allocations.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Seat Allocation Results</h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {allocations.map((allocation, index) => (
              <div key={index} className="border-2 border-gray-200 rounded-lg p-4 bg-gray-50 shadow-md">
                <h3 className="font-bold text-lg mb-2 text-blue-700 border-b border-blue-200 pb-1">
                  {allocation.room.name}
                </h3>
                <p className="text-sm text-gray-800 mb-3 font-medium">
                  Capacity: <span className="font-bold">{allocation.room.capacity}</span> | 
                  Allocated: <span className="font-bold text-green-600">{allocation.students.length}</span>
                </p>
                
                {/* Subject breakdown */}
                <div className="mb-3">
                  <p className="text-xs font-bold text-gray-800 mb-1">Subjects:</p>
                  <div className="flex flex-wrap gap-1">
                    {Object.entries(allocation.subject_breakdown).map(([subject, count]) => (
                      <span key={subject} className="text-xs bg-blue-200 text-blue-900 px-2 py-1 rounded-full font-medium">
                        {subject}: {count}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="space-y-1 max-h-48 overflow-y-auto">
                  {allocation.students.map((student, sIndex) => (
                    <div key={sIndex} className="text-xs bg-white p-2 rounded border border-gray-200">
                      <span className="font-bold text-gray-800">Seat {student.seat_number}:</span> <span className="text-gray-700">{student.student.name}</span>
                      <br />
                      <span className="text-gray-600">
                        {student.student.roll_number} - Y{student.student.year} - {student.student.subject}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-6 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div className="bg-white rounded-lg p-3 shadow-sm border border-blue-200">
                <div className="text-2xl font-bold text-blue-700">
                  {allocations.reduce((sum, allocation) => sum + allocation.students.length, 0)}
                </div>
                <div className="text-sm text-gray-700 font-medium">Students Allocated</div>
              </div>
              <div className="bg-white rounded-lg p-3 shadow-sm border border-green-200">
                <div className="text-2xl font-bold text-green-700">{allocations.length}</div>
                <div className="text-sm text-gray-700 font-medium">Rooms Used</div>
              </div>
              <div className="bg-white rounded-lg p-3 shadow-sm border border-purple-200">
                <div className="text-2xl font-bold text-purple-700">{subjects.length}</div>
                <div className="text-sm text-gray-700 font-medium">Subjects</div>
              </div>
              <div className="bg-white rounded-lg p-3 shadow-sm border border-orange-200">
                <div className="text-2xl font-bold text-orange-700">
                  {rooms.reduce((sum, room) => sum + room.capacity, 0) - 
                   allocations.reduce((sum, allocation) => sum + allocation.students.length, 0)}
                </div>
                <div className="text-sm text-gray-700 font-medium">Empty Seats</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExamSeatAllocator;