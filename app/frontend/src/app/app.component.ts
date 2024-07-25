import { Component, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ScrollProgressBarComponent } from './scroll-progress-bar/scroll-progress-bar.component';
import { LoadingService } from './loading.service';
import { DynamicComponentService } from './dynamic-component.service';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,
    ScrollProgressBarComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {

  @ViewChild('dynamicComponentContainer', { read: ViewContainerRef, static: true })
  dynamicComponentContainer!: ViewContainerRef;

  constructor(
    private loadingService: LoadingService,
    private dynamicComponentService: DynamicComponentService,
  ){}

  loadComponent(component: any) {
    this.dynamicComponentService.loadComponent(this.dynamicComponentContainer, component);
  }

  ngOnInit(){
    this.loadingService.simulateLoading();
  }
}
