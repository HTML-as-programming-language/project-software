#include <stdio.h>
#include <emscripten.h>
#include <emscripten/html5.h>

#define ARR_SIZE(arr) ( sizeof(arr) / sizeof(arr[0]) )

char *str[5];

void init_greetings() {
  str[0] = "Kikker";
  str[1] = "Meer kikkers";
  str[2] = "Flask";
  str[3] = "Angular";
  str[4] = "C code";
}

EM_BOOL mouse_callback(int eventType, const EmscriptenMouseEvent *e, void *userData)
{
  printf("%s. op positie (%ld, %ld)\n", str[(e->clientX + e->clientY) % ARR_SIZE(str)], e->clientX, e->clientY);
  return 0;
}

int main(int argc, char *argv[])
{
  init_greetings();

  printf("Hello from Angular\n");

  emscripten_set_click_callback(0, 0, 0, mouse_callback);
  return 0;
}
