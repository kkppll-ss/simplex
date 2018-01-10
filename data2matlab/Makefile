CC=g++
CXXFLAGS=-O2
LDFLAGS=
TARGET= data2matlab
OBJS = main.o
default:$(TARGET)
$(TARGET):$(OBJS)
	$(CC) -o $(TARGET) $(OBJS)
clean:
	rm -rf $(OBJS) $(TARGET)
