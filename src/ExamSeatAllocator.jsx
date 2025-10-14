import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Users, MapPin, Download, Book, Shuffle, AlertCircle } from 'lucide-react';
import ApiClient from './services/api';

const ExamSeatAllocator = () => {
  const [students, setStudents] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [allocations, setAllocations] = useState([]);
  const [currentStudent, setCurrentStudent] = useState({ name: '', roll_number: '', year: '', subjects: [] });
  const [currentRoom, setCurrentRoom] = useState({ name: '', capacity: '' });
  const [currentSubject, setCurrentSubject] = useState('');
  const [allocationStrategy, setAllocationStrategy] = useState('mixed'); // 'mixed' or 'separated'
  const [selectedAllocationSubject, setSelectedAllocationSubject] = useState(''); // For subject-specific allocation
  const [availableSubjects, setAvailableSubjects] = useState([]); // Subjects from students

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

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

    setLoading(true);
    try {
      await ApiClient.createRoom({
        name: currentRoom.name,
        capacity: parseInt(currentRoom.capacity)
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
              placeholder="Room Capacity"
              value={currentRoom.capacity}
              onChange={(e) => setCurrentRoom({...currentRoom, capacity: e.target.value})}
              className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800"
              disabled={loading}
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