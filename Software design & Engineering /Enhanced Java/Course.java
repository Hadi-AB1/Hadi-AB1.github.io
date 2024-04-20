public class Course {

	    // elements
		public String course; // raw data (String) of each row in this course file
		public String coName; // course name
		public String credit; // course credit
		public int num; // the number of total students
		public static int[] GraCount; // store students' number of each grade
		public static int highscore; // the highest score of the course
		public static int lowscore;  // the lowest score of the course
		public static double averscore;  // the average score of the course
		
		// constructor
		public Course() {
			
			// initialization
			course = coName = credit = "";
			num = highscore = 0;
			lowscore = 100;
			averscore = 0.0;
			GraCount = new int[]{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
		}
		
		
		// get course data
		public void getCourseData(String course) {
			
			// store data by using split array
			coName = course.split(",")[0];
			credit = course.split(",")[1];
		}
		
	
} // end the class
