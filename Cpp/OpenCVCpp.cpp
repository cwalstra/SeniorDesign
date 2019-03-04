#include <stdio.h>
#include <chrono>
#include <opencv2/opencv.hpp>
#include <raspicam/raspicam_cv.h>

using namespace std;
using namespace raspicam;
using namespace cv;

int main(int argc, char** argv )
{
    Mat image, output;
    raspicam::RaspiCam_Cv camera;
    cv::HOGDescriptor hog;
    hog.setSVMDetector(cv::HOGDescriptor::getDefaultPeopleDetector());
    std::vector<cv::Rect> found;

    if ( !camera.open() )
    {
        printf("No image data \n");
        return -1;
    }

    clock_t begin, end;
    while (1) {
       begin = clock();
       camera.grab();
       camera.retrieve(image);

       resize(image, output, cv::Size(400.0, 300.0), 0, 0, INTER_AREA);

       hog.detectMultiScale(output, found, 0, cv::Size(4,4), cv::Size(8, 8), 1.05, 2);

       for (int i = 0; i < found.size(); i++) {
           rectangle(output, found[i], (0, 0, 255), 2, 8, 0);
       }

       imshow("webcam input", output);
       char c = (char)waitKey(1);
       end = clock();
       printf("Elapsed time: %da\n", end - begin);
       if ( c==27 ) break;
    }

    printf("Clocks per second: %d", CLOCKS_PER_SEC);
    printf("Clocks per second: %f", float(end - begin)/CLOCKS_PER_SEC);
    return 0;
}
