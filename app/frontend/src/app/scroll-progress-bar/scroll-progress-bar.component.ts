import { Component, OnInit } from '@angular/core';
import { LoadingService } from '../loading.service';

@Component({
  selector: 'app-scroll-progress-bar',
  standalone: true,
  templateUrl: './scroll-progress-bar.component.html',
  styleUrls: ['./scroll-progress-bar.component.css'],
})
export class ScrollProgressBarComponent implements OnInit {
  scrollPercentage: number = 0; // Initialize to 0

  constructor(private loadingService: LoadingService) {}

  ngOnInit() {
    this.loadingService.loadingProgress$.subscribe(progress => {
      this.scrollPercentage = progress;
    })
  }
}
