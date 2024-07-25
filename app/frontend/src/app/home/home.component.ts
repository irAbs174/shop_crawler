import { Component, OnInit, ViewChild, ViewContainerRef, NgModule } from '@angular/core';
import { LoadingService } from '../loading.service';
import { DynamicComponentService } from '../dynamic-component.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    FormsModule,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  @ViewChild('dynamicComponentContainer', { read: ViewContainerRef, static: true })
  dynamicComponentContainer!: ViewContainerRef;

  constructor(
    private loadingService: LoadingService,
  ){}

  homeHiddenClass = false;

  ngOnInit(): void {
    this.loadingService.simulateLoading()
  }

}
