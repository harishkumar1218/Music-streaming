int current_x;
int current_y;
int destination_x;
int destination_y;

int visited_x[25];
int visited_y[25];
int visited_count = 0;

int path_x[25];
int path_y[25];
int path_count = 0;

int obstacle_x[5] = {4,3,3};
int obstacle_y[5] = {5,4,3};

float a, b, c, d;

int isVisited(int x, int y){
  int flag = 0;
  for (int i = 0;i < visited_count;i++){
    if (visited_x[i] == x && visited_y[i] == y){
      flag = 1;
    }
  }
  if (flag == 1){
    return 1;
  }
  else{
    return 0;
  }
}


int isObstacle(int x, int y){
  int flag = 0;
  for (int i = 0;i < 4;i++){
    if (obstacle_x[i] == x && obstacle_y[i] == y){
      flag = 1;
    }
  }
  if (flag == 1){
    return 1;
  }
  else{
    return 0;
  }
}
float dist(int x, int y){
  if (x > 5 || y > 5 || x < 1 || y < 1 || isVisited(x, y) || isObstacle(x, y)){
    return 100;
  }
  else{
    float dist;
    dist = (destination_x-x)*(destination_x-x) + (destination_y-y)*(destination_y-y);
    return dist;
  }
}


void setup() {
  Serial.begin(9600);



  /*Serial.println("Enter start_x:");
  while (Serial.available() == 0){}
  current_x = Serial.parseInt();
  Serial.println("Enter start_y:");
  while (Serial.available() == 0){}
  current_y = Serial.parseInt();

  Serial.println("Enter destination_x:");
  while (Serial.available() == 0){}
  destination_x = Serial.parseInt();
  Serial.println("Enter destination_y:");
  while (Serial.available() == 0){}
  destination_y = Serial.parseInt();*/

  current_x = 3;
  current_y = 1;

  destination_x = 3;
  destination_y = 5;

  visited_x[visited_count] = current_x;
  visited_y[visited_count] = current_y;
  visited_count++;

  path_x[path_count] = current_x;
  path_y[path_count] = current_y;
  path_count++;

  while (current_x != destination_x || current_y != destination_y){
    Serial.print("Current_x: ");
    Serial.println(current_x);
    Serial.print("Current_y: ");
    Serial.println(current_y);
    Serial.print("Path Count: ");
    Serial.println(path_count);
    
    a = dist(current_x, current_y+1);
    Serial.print("a = ");
    Serial.println(a);
    b = dist(current_x+1, current_y);
    Serial.print("b = ");
    Serial.println(b);
    c = dist(current_x, current_y-1);
    Serial.print("c = ");
    Serial.println(c);
    d = dist(current_x-1, current_y);
    Serial.print("d = ");
    Serial.println(d);
    if (a == 100 && b == 100 && c == 100 && d == 100){
      path_count--;

      if (path_count == -1){
        Serial.println("PATH DOESN'T EXIST");
        break;
      }
      else{
        current_x = path_x[path_count-1];
        current_y = path_y[path_count-1];
        
        Serial.print("New x: ");
        Serial.println(current_x);
        Serial.print("New Y: ");
        Serial.println(current_y);
        continue;
      }
    }

    else{
      if (a <= b && a <= c && a <= d){
        visited_x[visited_count] = current_x;
        visited_y[visited_count] = current_y+1;
        visited_count++;

        path_x[path_count] = current_x;
        path_y[path_count] = current_y+1;
        path_count++;

        current_x = current_x;
        current_y = current_y+1;
        continue;
        
      }
      else if (b <= a && b <= c && b <= d){
        visited_x[visited_count] = current_x+1;
        visited_y[visited_count] = current_y;
        visited_count++;

        path_x[path_count] = current_x+1;
        path_y[path_count] = current_y;
        path_count++;

        current_x = current_x+1;
        current_y = current_y;
        continue;
      }
      else if (c <= a && c <= b && c <= d){
        visited_x[visited_count] = current_x;
        visited_y[visited_count] = current_y-1;
        visited_count++;

        path_x[path_count] = current_x;
        path_y[path_count] = current_y-1;
        path_count++;

        current_x = current_x;
        current_y = current_y-1;
        continue;
      }
      else if (d <= a && d <= b && d <= c){
        visited_x[visited_count] = current_x-1;
        visited_y[visited_count] = current_y;
        visited_count++;

        path_x[path_count] = current_x-1;
        path_y[path_count] = current_y;
        path_count++;

        current_x = current_x-1;
        current_y = current_y;
        continue;
      }
    }
  }

  for (int i = 0;i < path_count;i++){
    Serial.print(path_x[i]);
    Serial.print(", ");
    Serial.print(path_y[i]);
    Serial.println();
  }

}


void loop(){}