import { TestBed } from '@angular/core/testing';

import { LoaddingService } from './loading.service';

describe('LoaddingService', () => {
  let service: LoaddingService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoaddingService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
