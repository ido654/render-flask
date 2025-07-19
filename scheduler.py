from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class ShiftEntry:
    user_id: int
    shift_id: int
    available_key: int
    score: float = field(init=False)

    def __post_init__(self):
        if self.available_key == 1:
            self.score = 0.5
        elif self.available_key == 2:
            self.score = 1.0
        elif self.available_key == 3:
            self.score = 1.5
        else:
            self.score = 0.0


def assign_initial_shifts(data: List[ShiftEntry], users_per_shift: int = 2) -> Tuple[Dict[int, List[int]], Dict[int, float], Dict[int, int]]:
    """Assigns initial shifts based on lowest adjusted score."""
    assignments = defaultdict(list)
    user_shift_counts = defaultdict(int)
    user_cumulative_scores = defaultdict(float)

    shift_ids = sorted(set(entry.shift_id for entry in data))

    for shift_id in shift_ids:
        # Filter candidates for current shift
        candidates = [
            entry for entry in data
            if entry.shift_id == shift_id and entry.available_key > 0
        ]

        # Add adjusted score
        for candidate in candidates:
            candidate.adjusted_score = candidate.score + user_shift_counts[candidate.user_id]

        # Sort candidates by adjusted score
        candidates.sort(key=lambda c: c.adjusted_score)

        for candidate in candidates[:users_per_shift]:
            assignments[shift_id].append(candidate.user_id)
            user_shift_counts[candidate.user_id] += 1
            user_cumulative_scores[candidate.user_id] += candidate.adjusted_score + 1  # includes "cost"

    return assignments, user_cumulative_scores, user_shift_counts


def optimize_assignments(assignments: Dict[int, List[int]],
                         data: List[ShiftEntry],
                         cumulative_scores: Dict[int, float],
                         shift_counts: Dict[int, int]) -> Tuple[Dict[int, List[int]], Dict[int, int], Dict[int, float]]:
    """Optimizes assignment by swapping high-cost users with better candidates."""
    shift_ids = sorted(assignments.keys())
    data_lookup = {(d.shift_id, d.user_id): d for d in data}

    changed = True
    while changed:
        changed = False

        for shift_id in shift_ids:
            current_users = assignments[shift_id]
            candidates = [
                entry for entry in data
                if entry.shift_id == shift_id and entry.available_key > 0 and entry.user_id not in current_users
            ]

            for candidate in candidates:
                candidate_score_cost = candidate.score + 1

                for i, current_user_id in enumerate(current_users):
                    current_entry = data_lookup.get((shift_id, current_user_id))
                    if not current_entry:
                        continue

                    current_score = cumulative_scores[current_user_id]
                    candidate_adjusted_score = cumulative_scores[candidate.user_id] + candidate_score_cost

                    if current_score > candidate_adjusted_score:
                        # Swap
                        changed = True
                        current_users[i] = candidate.user_id

                        cumulative_scores[current_user_id] -= current_entry.score + 1
                        cumulative_scores[candidate.user_id] += candidate_score_cost

                        shift_counts[current_user_id] -= 1
                        shift_counts[candidate.user_id] += 1
                        break

    return assignments, shift_counts, cumulative_scores


def run_scheduling(raw_data: List[Dict]) -> Dict[str, Dict]:
    """Main function to run the full scheduling process."""
    data = [ShiftEntry(**item) for item in raw_data]
    assignments, cumulative_scores, shift_counts = assign_initial_shifts(data)
    assignments, shift_counts, cumulative_scores = optimize_assignments(assignments, data, cumulative_scores, shift_counts)
    return {
        'assignments': dict(assignments),
        'cumulative_score': dict(cumulative_scores),
        'user_shifts_count': dict(shift_counts)
    }

if __name__ == "__main__":
    input_data = [
        {'user_id' : 1 , 'shift_id' : 1 , 'available_key' : 2},
        {'user_id' : 2 , 'shift_id' : 1 , 'available_key' : 1},
        {'user_id' : 3 , 'shift_id' : 1 , 'available_key' : 2},
        {'user_id' : 1 , 'shift_id' : 2 , 'available_key' : 1},
        {'user_id' : 3 , 'shift_id' : 2 , 'available_key' : 2},
        {'user_id' : 2 , 'shift_id' : 2 , 'available_key' : 2},
    ]

    result = run_scheduling(input_data)
    print(result)


