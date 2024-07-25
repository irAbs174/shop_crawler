import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LoadingService {
  private loadingProgress = new BehaviorSubject<number>(0);
  loadingProgress$ = this.loadingProgress.asObservable();

  simulateLoading() {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 12;
      this.loadingProgress.next(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 100); // Adjust the interval duration as needed
  }
}
