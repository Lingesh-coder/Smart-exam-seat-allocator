# Testing the Enhanced Seat Allocation System

## Prerequisites
1. Make sure you have Python installed with required packages
2. Install any missing dependencies in the backend

## Step 1: Start the Backend Server
```bash
cd "c:\Users\Lingesh\Desktop\Mini project\backend"
python app.py
```

## Step 2: Test the Enhanced Features
In a new terminal:
```bash
cd "c:\Users\Lingesh\Desktop\Mini project"
python demo_csv_import.py
```

## Step 3: Start the Frontend (Optional)
In another terminal:
```bash
cd "c:\Users\Lingesh\Desktop\Mini project"
npm run dev
```

## What to Expect

### Enhanced Algorithm Features:
1. **Better Subject Separation**: Students with the same subjects will be placed further apart
2. **Quality Metrics**: Each allocation will show distribution and separation scores
3. **Spatial Awareness**: The algorithm considers 2D room layout for optimal placement
4. **Multi-Pass Allocation**: Three-phase allocation for maximum efficiency

### Improved PDF Reports:
1. **Dual Subject Columns**: 
   - Primary Subject: Shows the main subject for quick reference
   - All Subjects: Shows complete subject list with smart formatting
2. **Better Layout**: 
   - Alternating row colors for better readability
   - Optimized column widths for subject information
   - Better alignment and typography
3. **Quality Metrics**: 
   - Distribution scores per room
   - Separation quality ratings
   - Overall quality assessment

### Demo Output Examples:
```
🔬 Testing MIXED strategy...
✅ Mixed allocation successful:
   - Allocation ID: 507f1f77bcf86cd799439011
   - Students Allocated: 18/20
   - Allocation Rate: 90.0%
   - Quality Rating: Very Good
   - Distribution Score: 2.5
   - Separation Score: 3.2
   - Algorithm Version: advanced_v3.0
📄 Testing PDF generation for mixed strategy...
✅ PDF generated successfully (15234 bytes)
```

## Testing Different Scenarios

### 1. Test with Subject Filter
```python
allocation_data = {
    'strategy': 'mixed',
    'subject_filter': 'CS101'  # Filter for specific subject
}
```

### 2. Compare Strategies
- **Mixed Strategy**: Distributes different subjects across rooms
- **Separated Strategy**: Groups subjects by room but separates within rooms

### 3. Check Quality Metrics
- **Distribution Score**: Higher = better subject spread
- **Separation Score**: Higher = better spatial separation
- **Quality Rating**: Overall assessment of allocation quality

## Troubleshooting

### If Backend Won't Start:
1. Check Python version: `python --version`
2. Install requirements: `pip install -r backend/requirements.txt`
3. Check MongoDB connection
4. Verify port 5000 is available

### If Demo Script Fails:
1. Ensure backend is running on http://localhost:5000
2. Check network connectivity
3. Verify API endpoints are accessible

### If PDF Generation Fails:
1. Install reportlab: `pip install reportlab`
2. Check file permissions
3. Verify temporary directory access

## Manual Testing via Web Interface

1. Open http://localhost:5174 (frontend)
2. Upload CSV files using the interface
3. Create allocations with different strategies
4. Download PDF reports to see enhanced formatting
5. Compare quality metrics between strategies

## Expected Improvements

### Algorithm Performance:
- Better distribution of subjects across seats
- Improved spatial separation (especially in larger rooms)
- Higher quality ratings overall
- More consistent allocation results

### PDF Quality:
- Clearer subject information display
- Better visual organization
- Quality metrics for assessment
- Professional report formatting