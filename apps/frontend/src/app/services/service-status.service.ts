import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServiceStatusService {
  private backendOfflineSubject = new BehaviorSubject<boolean>(false);
  private llamaOfflineSubject = new BehaviorSubject<boolean>(false);

  backendOffline$ = this.backendOfflineSubject.asObservable();
  llamaOffline$ = this.llamaOfflineSubject.asObservable();

  markBackendOffline(): void {
    this.backendOfflineSubject.next(true);
  }

  markBackendOnline(): void {
    this.backendOfflineSubject.next(false);
  }

  markLlamaOffline(): void {
    this.llamaOfflineSubject.next(true);
  }

  markLlamaOnline(): void {
    this.llamaOfflineSubject.next(false);
  }
}
