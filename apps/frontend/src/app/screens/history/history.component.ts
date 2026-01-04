import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {TripHistoryService} from '../../services/trip-history.service';
import {RecommendationService} from '../../services/recommendation.service';
import {TripOverview} from '../../data-model/tripOverview';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {
  trips: TripOverview[] | null = null;
  loading = true;
  error?: string;
  deletingTripId?: string;
  selectMode = false;
  selectedTripIds = new Set<string>();
  bulkDeleting = false;
  bulkError?: string;
  bulkFailedIds: string[] = [];

  constructor(private tripHistoryService: TripHistoryService,
              private recommendationService: RecommendationService,
              private router: Router) {}

  ngOnInit(): void {
    this.tripHistoryService.getTripHistoryOverview().subscribe(trips => {
      this.trips = trips;
      this.loading = false;
      if (trips === null) {
        this.error = 'Unable to load trip history.';
      }
    });
  }

  goToTrip(trip: TripOverview): void {
    this.recommendationService.getTripFromHistory(trip.trip_id);
    this.router.navigate(['/trip']);
  }

  deleteTrip(trip: TripOverview): void {
    this.deletingTripId = trip.trip_id;
    this.tripHistoryService.deleteTrip(trip.trip_id).subscribe(success => {
      this.deletingTripId = undefined;
      if (!success) {
        this.error = 'Unable to remove trip.';
        return;
      }
      if (this.trips) {
        this.trips = this.trips.filter(item => item.trip_id !== trip.trip_id);
      }
      if (this.selectedTripIds.has(trip.trip_id)) {
        this.selectedTripIds.delete(trip.trip_id);
      }
    });
  }

  toggleSelectMode(): void {
    this.selectMode = !this.selectMode;
    this.clearSelection();
  }

  toggleTripSelection(trip: TripOverview, checked: boolean): void {
    if (checked) {
      this.selectedTripIds.add(trip.trip_id);
    } else {
      this.selectedTripIds.delete(trip.trip_id);
    }
  }

  selectAllTrips(): void {
    if (!this.trips) {
      return;
    }
    this.selectedTripIds = new Set(this.trips.map(trip => trip.trip_id));
  }

  clearSelection(): void {
    this.selectedTripIds.clear();
    this.bulkError = undefined;
    this.bulkFailedIds = [];
  }

  deleteSelectedTrips(): void {
    if (this.selectedTripIds.size === 0 || this.bulkDeleting) {
      return;
    }
    const confirmed = window.confirm('Delete all selected trips? This cannot be undone.');
    if (!confirmed) {
      return;
    }
    this.bulkDeleting = true;
    this.bulkError = undefined;
    this.bulkFailedIds = [];
    const tripIds = Array.from(this.selectedTripIds);
    this.tripHistoryService.deleteTrips(tripIds).subscribe(response => {
      this.bulkDeleting = false;
      if (!response.success) {
        this.bulkFailedIds = response.missing_ids || [];
        const missingLabel = this.bulkFailedIds.length > 0
          ? ` Missing trips: ${this.bulkFailedIds.join(', ')}.`
          : '';
        const errorDetails = response.errors && response.errors.length > 0
          ? ` ${response.errors.join(' ')}`
          : '';
        this.bulkError = `Unable to delete selected trips.${missingLabel}${errorDetails}`;
        return;
      }
      if (this.trips) {
        this.trips = this.trips.filter(item => !this.selectedTripIds.has(item.trip_id));
      }
      this.clearSelection();
      this.selectMode = false;
    });
  }

  isTripSelected(trip: TripOverview): boolean {
    return this.selectedTripIds.has(trip.trip_id);
  }

  get selectedCount(): number {
    return this.selectedTripIds.size;
  }

  getTripDatesLabel(trip: TripOverview): string | null {
    if (!trip.dates || trip.dates.length === 0) {
      return null;
    }
    const dates = trip.dates.map(date => new Date(date));
    const start = this.formatDate(dates[0]);
    if (trip.days_len <= 1 || dates.length < 2) {
      return start;
    }
    const end = this.formatDate(dates[1]);
    return `${start} - ${end}`;
  }

  private formatDate(date: Date): string {
    if (Number.isNaN(date.getTime())) {
      return '';
    }
    return date.toLocaleDateString();
  }
}
