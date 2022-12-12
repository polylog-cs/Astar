/* Written by Filip Hlasek 2022 */
#include <set>
#include <map>
#include <queue>
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <random>
using namespace std;

const uint8_t BOARD_SIZE = 4;
const uint8_t CELLS = BOARD_SIZE * BOARD_SIZE;

const int MOVES[4][2] = {{-1, 0}, {0, -1}, {1, 0}, {0, 1}};


struct BoardState {
  // Values are stored row-by-row, 0 representing an empty cell.
  //std::vector<uint8_t> values;

    unsigned long long values;

  bool operator<(const BoardState& other) const {
    return values < other.values;
  }
  
  bool operator==(const BoardState& other) const {
    return values == other.values;
  }

    BoardState(vector<int> perm){
        values = 0;
    for (int i = 0; i < BOARD_SIZE; ++i) {
      for (int j = 0; j < BOARD_SIZE; ++j) {
        set_cell(i, j, perm[i*BOARD_SIZE + j]);
      }
    }     
    }

  // Returns the value of the cell in the given row and column
  uint8_t cell(int row, int col) const {
    return  ( values >> ( (row * BOARD_SIZE + col)*4 ) ) % 16;
  }

    void set_cell(int row, int col, int val){
        int cur = cell(row, col);
        values -= ( (long long ) cur) << ( (row * BOARD_SIZE + col)*4 );
        values += ( (long long ) val) << ( (row * BOARD_SIZE + col)*4 );
    }

  void swapCells(int row1, int col1, int row2, int col2) {
    int val1 = cell(row1, col1);
    int val2 = cell(row2, col2);
    set_cell(row1, col1, val2);
    set_cell(row2, col2, val1);
  }

  void debugPrint() const {
    std::cerr << "BoardState: " << std::endl;
    for (int i = 0; i < BOARD_SIZE; ++i) {
      for (int j = 0; j < BOARD_SIZE; ++j) {
        std::cerr << "\t" << (int)cell(i, j);
      }
      std::cerr << std::endl;
    }
  }

  std::pair<uint8_t, uint8_t> findEmptyCell() const {
    for (int i = 0; i < BOARD_SIZE; ++i) {
      for (int j = 0; j < BOARD_SIZE; ++j) {
        if (cell(i, j) == 0) {
          return std::make_pair(i, j);
        }
      }
    }
    // There should always be an empty cell;
    std::cerr << "This state has no empty cell!!!." << std::endl;
    debugPrint();
    return std::make_pair(0, 0);
  }

  // The resulting vector has on i-th position the coordinates of the value i.
  std::vector<std::pair<int, int>> valueCoordinates() const {
    std::vector<std::pair<int, int>> result(CELLS);
    for (int i = 0; i < BOARD_SIZE; ++i) {
      for (int j = 0; j < BOARD_SIZE; ++j) {
        result[cell(i, j)] = std::make_pair(i, j);
      }
    }
    return result;
  }

  vector<int> get_permutation() const{
    vector<int> ret = {};
    for (int i = 0; i < BOARD_SIZE; ++i) {
      for (int j = 0; j < BOARD_SIZE; ++j) {
        ret.push_back(cell(i,j));
      }
    }
    return ret;
  }

};


//https://cp-algorithms.com/others/15-puzzle.html#implementation
bool parity(const BoardState& a){
    int inv = 0;
    vector<int> perm = a.get_permutation();
    for (int i=0; i<16; ++i)
        if (perm[i])
            for (int j=0; j<i; ++j)
                if (perm[j] > perm[i])
                    ++inv;
    for (int i=0; i<16; ++i)
        if (perm[i] == 0)
            inv += 1 + i / 4;

    return inv & 1;
}

/**
 * This function computes an A* heuristic. Specifically, it assumes that each number
 * can be shifted along the shortest path to its destination without having to
 * worry about other numbes. Since in the actual game each move shifts two numbers
 * in the end we need to divide the result by two.
 * Note: if the resulting value is odd, it proves that the position cannot be reached
 * using the allowed moves. We ignore that case in our implementation.
 */
int aStarHeuristic(const BoardState& a, const BoardState& b) {
  auto coords_a = a.valueCoordinates(), coords_b = b.valueCoordinates();
  int ans = 0;
  for (int value = 1; value < CELLS; ++value) {
    ans += abs(coords_a[value].first - coords_b[value].first);
    ans += abs(coords_a[value].second - coords_b[value].second);
  }
  return ans;
}

int dijkstra(const BoardState start, const BoardState goal, bool use_a_star_heuristic=false) {
  // For each state, we maintain what is the minimum possible number of steps
  // to reach that state.
  map<BoardState, int> min_steps_to_reach;

  // We maintain a priority queue of states the first value in the pair
  // is the number by which we want to visit the states.
  priority_queue< pair<int, BoardState> > queue;

  // We keep track of which states are considered done.
  set<BoardState> finished;

  min_steps_to_reach[start] = 0;
  queue.push(make_pair(0, start));

  long long iterations = 0;
  while (!queue.empty()) {
    auto state = queue.top().second;
    queue.pop();
    if (finished.find(state) != finished.end()) {
        min_steps_to_reach.erase(state);
      continue;
    }
    finished.insert(state);


    auto distance = min_steps_to_reach[state];

    if (++iterations % 1000000 == 0) {
      cerr << "Iterations: " << iterations << ", " << min_steps_to_reach.size() << ", " << queue.size() << ", " << distance << ", " << distance + aStarHeuristic(state, goal) << endl;
    }

    if (state.values == goal.values) {
      cerr << "Path to goal state found!" << endl;
      cerr << "Distance: " << distance << endl;
      cerr << "Iterations: " << iterations << endl << endl;
      break;
    }

    int row, col;
    tie(row, col) = state.findEmptyCell();
    for (int move = 0; move < 4; ++move) {
      int new_row = row + MOVES[move][0], new_col = col + MOVES[move][1];
      if (new_row < 0 || new_row >= BOARD_SIZE || new_col < 0 || new_col >= BOARD_SIZE) {
        continue;
      }
      // Update the state for now, we will revert this change later
      state.swapCells(row, col, new_row, new_col);

      auto new_distance = distance + 1;

      if (min_steps_to_reach.find(state) == min_steps_to_reach.end()
          || min_steps_to_reach[state] > new_distance) {
        min_steps_to_reach[state] = new_distance;

        auto potential = new_distance;
        if (use_a_star_heuristic) {
          potential += aStarHeuristic(state, goal);
        }
        // We store the distances in the priority queue with a negative sign so that
        // we get the smallest distances on the top.
        queue.push(make_pair(-potential, state));
      }

      // Revert the swap as promised above.
      state.swapCells(row, col, new_row, new_col);

      
    }
    min_steps_to_reach.erase(state);
  }

  return iterations;
}

int main(int argc, char* argv[]) {
  BoardState start_test({
    4, 6, 7, 2,
    8, 3, 11, 0,
    1, 5, 14, 10,
    9, 12, 13, 15
  });

  // This state should be solvable in 26 steps.

  BoardState goal({
    0, 1, 2, 3,
    4, 5, 6, 7,
    8, 9, 10, 11,
    12, 13, 14, 15
  });


    int max_it = 10;
    int num = 0;
    mt19937 g(0); 
    for(int it = 0; it < max_it; ++it){
        // random starting state

        vector<int> perm = vector<int>(16, 0);
        for(int i = 0; i < 16; ++i){perm[i] = i;}
        do{
            shuffle(perm.begin(), perm.end(), g);
        }while(parity(goal) != parity(BoardState(perm)));

        BoardState start_random(perm);

        start_random.debugPrint();
        num += dijkstra(start_random, goal, true);

    }

    cout << "average number of explored nodes: " << (double)num / max_it << endl;
  return 0;
}