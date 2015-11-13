#ifndef COMMON_CHANNEL_CHANNEL_H
#define COMMON_CHANNEL_CHANNEL_H

#include <functional>
#include <vector>

class Channel {
public:
  typedef std::vector<char> Buffer;
  typedef std::function<void(Buffer, std::size_t)> CallbackFunction;

  //virtual int Read(buffer& buffer) = 0;
  //register listener, listend to function is invoked if something is read
  //from the underlying socket
  virtual void OnRead(CallbackFunction callback) = 0;
  virtual void Write(Buffer& buffer) = 0;
  virtual void Close() = 0;
};

#endif
