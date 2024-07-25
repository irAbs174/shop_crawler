import { Component, OnInit, ViewChild, ViewContainerRef, NgModule } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ScrollProgressBarComponent } from './scroll-progress-bar/scroll-progress-bar.component';
import { DynamicComponentService } from './dynamic-component.service';
import { AuthComponent } from './auth/auth.component';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    ScrollProgressBarComponent,
    AuthComponent,
    FormsModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {

  @ViewChild('dynamicComponentContainer', { read: ViewContainerRef, static: true })
  dynamicComponentContainer!: ViewContainerRef;

  constructor(
    private dynamicComponentService: DynamicComponentService,
  ){}

  loadComponent(component: any) {
    this.dynamicComponentService.loadComponent(this.dynamicComponentContainer, component);
  }

  ngOnInit(): void {
    this.loadComponent(AuthComponent)
  }
}
