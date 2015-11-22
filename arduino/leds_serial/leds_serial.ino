
int leds[] = {5, 6, 7}; // Serial port of leds
char serial_buffer[255];
int serial_count = 0;
void setup() {                
  Serial.begin(9600);  
  for(int i=0; i< sizeof(leds); i++){
      pinMode(leds[i], OUTPUT);
  }
}

void buffer_clean(){
  for (int cl=0; cl<=serial_count; cl++){
    serial_buffer[cl]=0;
  }
  serial_count = 0;
}


void manage_leds(char *string){
  char action_on[10];
  char action_off[10];  
  for(int i=0; i < sizeof(leds); i++){
    sprintf(action_on, "led%d on", i);
    sprintf(action_off, "led%d off", i);
    if (strstr(string, action_on) != 0){
      digitalWrite(leds[i], HIGH);  
    }else if (strstr(string, action_off) != 0){
      digitalWrite(leds[i], LOW);
    }      
  }
}


void loop() {
 
  if(Serial.available() > 0){
    char dato = Serial.read();
    serial_buffer[serial_count++]=dato;
    if (dato == '\n'){
      Serial.print(serial_buffer);
      manage_leds(serial_buffer);     
      buffer_clean();
    }  
  } 
}
