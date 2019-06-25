#include <iostream>
#include <fstream>
// Do not delete this @ tag
// @namespace footrack

namespace footrack {

// Definition

// Default buffer size is 10000;
const int kDefaultBufferSize = 10000;

class FooTracker {
  public:
    FooTracker(int buffer_size = kDefaultBufferSize);
    ~FooTracker();
    void log(int64_t index);
    void dump2file();
    void dump(int n = 10);
  private:
    int buffer_size_;
    int64_t* buffer_head_ = nullptr;
    int cursor_ = 0;
    bool buffer_reused_ = false;
};

// Implementation

FooTracker::FooTracker(int buffer_size)
     : buffer_size_(buffer_size),  
       buffer_head_(nullptr) {
    std::cout << "FooTracker init." << std::endl;
    std::cout << "size = " << buffer_size_ << std::endl;
    // TODO: buffer_size <= 0 case
    buffer_head_ = new int64_t[buffer_size];
    std::cout << "buffer head = " << buffer_head_ << std::endl;
}

FooTracker::~FooTracker() {
  if(buffer_head_ != nullptr) {
    delete buffer_head_;
    buffer_head_ = nullptr;
  }
}

void FooTracker::log(int64_t index) {
    //std::cout << "FooTracker log(" << index << ")." << std::endl;
    buffer_head_[cursor_++] = index;
    if(cursor_ >= buffer_size_) {
        std::cout << "FooTracker buffer finish. will reuse the fuffer from start."
                  << std::endl;
        cursor_ = 0;
        buffer_reused_ = true;
    }
}

void FooTracker::dump2file() {
    std::cout << "FooTracker dump2file()." << std::endl;
    std::ofstream outfile;
    outfile.open("footrackstat.dat");
    // If all buffer is used then set start point as cursor_
    // If buffer is not finish then start point is 0, end point is cursor - 1
    if(buffer_reused_) {
        for(int i = cursor_; i < buffer_size_; i++) {
            outfile << buffer_head_[i] << ' '; 
        }
        for(int i = 0;i < cursor_; i++) {
            outfile << buffer_head_[i] << ' '; 
        }
    }
    else { 
        for(int i = 0;i < cursor_; i++) {
            outfile << buffer_head_[i] << ' '; 
        } 
    }
    outfile.close();
}

void FooTracker::dump(int n) {
    int count = 0;
    // If all buffer is used then set start point as cursor_
    // If buffer is not finish then start point is 0, end point is cursor - 1
    if(buffer_reused_) {
        for(int i = cursor_; i < buffer_size_; i++) {
            std::cout << buffer_head_[i] << ' '; 
            if(count++ > n)return;
        }
        for(int i = 0;i < cursor_; i++) {
            std::cout << buffer_head_[i] << ' '; 
            if(count++ > n)return;
        }
    }
    else { 
        for(int i = 0;i < cursor_; i++) {
            std::cout << buffer_head_[i] << ' '; 
            if(count++ > n)return;
        } 
    }
    std::cout << std::endl;
}


} // namespace fooltrack

// Do not delete this @ tag
// @namespace footrack end

// Do not delete this @ tag
// @interface footrack
footrack::FooTracker* fooTracker = nullptr;
void initFooTracker() {
    if(fooTracker) {
        std::cout << "fooTracker is initialized already"  << std::endl;
        return;
    }
    fooTracker = new footrack::FooTracker();
}

void fooTrackerLog(long long int index) {
    if(!fooTracker) {
        std::cout << "fooTracker pointer null!!! index(" << index << ")"  << std::endl;
        return;
    }
    fooTracker->log(index);
}

void dumpFooTrackInfo() {
    if(!fooTracker) {
        std::cout << "fooTracker pointer null!!! dump fooTrack info failure!"  << std::endl;
        return;
    }
    fooTracker->dump();
    fooTracker->dump2file();
}
// Do not delete this @ tag
// @interface footrack end


using namespace std;

void a(){
   cout << "a()" << endl; 
}

int b(){
   cout << "b()" << endl; 
   return 2;
}


void test1_b();
void test1_a();

int main(){

   fooTracker = new footrack::FooTracker(20);

   b();
   a();
   test1_b();
   test1_b();
   test1_b();
   b();
   a();
   b();
   a();
   test1_b();
   test1_a();
   b();
   a();
   dumpFooTrackInfo();
   delete fooTracker;
}
