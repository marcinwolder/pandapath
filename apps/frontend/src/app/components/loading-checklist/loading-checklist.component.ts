import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  Output,
  SimpleChanges
} from '@angular/core';

type StepState = 'pending' | 'active' | 'done';
type RunPhase = 'running' | 'waiting' | 'fast-forward' | 'completed';

interface ChecklistStep {
  key: string;
  label: string;
  detail?: string;
  minMs: number;
  maxMs: number;
}

interface ChecklistStepState extends ChecklistStep {
  duration: number;
  state: StepState;
}

@Component({
  selector: 'app-loading-checklist',
  templateUrl: './loading-checklist.component.html',
  styleUrls: ['./loading-checklist.component.css']
})
export class LoadingChecklistComponent implements OnInit, OnDestroy, OnChanges {
  @Input() cancelled = false;
  @Input() ready = false;
  @Input() waitForReadyIndex = 2;
  @Input() steps: ChecklistStep[] = [
    {
      key: 'analyze-preferences',
      label: 'Semantic Preference Mapping',
      detail: 'Extracting latent user constraints and intent via high-dimensional embedding analysis.',
      minMs: 900,
      maxMs: 1400
    },
    {
      key: 'select-attractions',
      label: 'Geospatial Candidate Filtering',
      detail: 'Pruning the Point-of-Interest (POI) search space using k-d tree spatial indexing.',
      minMs: 900,
      maxMs: 1400
    },
    {
      key: 'arrange-days',
      label: 'Multi-Objective Route Optimization',
      detail: 'Solving the Orienteering Problem (OP) with time-window constraints using meta-heuristic algorithms.',
      minMs: 800,
      maxMs: 1300
    },
    {
      key: 'apply-algorithms',
      label: 'Temporal Constraint Validation',
      detail: 'Verifying sequence feasibility against real-time opening hours and transit bottlenecks.',
      minMs: 1000,
      maxMs: 1500
    },
    {
      key: 'write-descriptions',
      label: 'NLG Narrative Synthesis',
      detail: 'Generating coherent daily summaries using a Large Language Model (LLM) for semantic enrichment.',
      minMs: 1000,
      maxMs: 1500
    }
  ];

  @Output() completed = new EventEmitter<void>();

  stepsState: ChecklistStepState[] = [];
  activeIndex = -1;

  private timerHandle: number | null = null;
  private completedEmitted = false;
  private phase: RunPhase = 'running';
  private readyReceived = false;

  ngOnInit(): void {
    this.resetSteps();
    if (this.ready) {
      this.readyReceived = true;
      this.phase = 'fast-forward';
    }
    this.runStep(0);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['ready'] && this.ready) {
      this.handleReady();
    }
    if (changes['cancelled'] && this.cancelled) {
      this.clearTimer();
    }
  }

  ngOnDestroy(): void {
    this.clearTimer();
  }

  get progressPercent(): string {
    const total = this.stepsState.length || 1;
    const doneCount = this.stepsState.filter(step => step.state === 'done').length;
    const inProgress = this.activeIndex >= 0 && this.activeIndex < total ? 0.4 : 0;
    const percent = Math.min(100, ((doneCount + inProgress) / total) * 100);
    return `${percent}%`;
  }

  private resetSteps(): void {
    this.stepsState = this.steps.map(step => ({
      ...step,
      duration: this.randomDuration(step.minMs, step.maxMs),
      state: 'pending'
    }));
    this.activeIndex = -1;
    this.completedEmitted = false;
    this.phase = 'running';
    this.readyReceived = false;
    this.clearTimer();
  }

  private runStep(index: number): void {
    if (this.cancelled) {
      return;
    }
    if (index >= this.stepsState.length) {
      this.emitCompleted();
      return;
    }

    this.activeIndex = index;
    this.stepsState[index].state = 'active';

    if (this.shouldWaitForReady(index)) {
      this.phase = 'waiting';
      this.clearTimer();
      return;
    }
    const duration = this.shouldFastForwardStep(index)
      ? this.fastDuration()
      : this.stepsState[index].duration;
    this.clearTimer();
    this.timerHandle = window.setTimeout(() => {
      this.stepsState[index].state = 'done';
      this.runStep(index + 1);
    }, duration);
  }

  private fastDuration(): number {
    return 500;
  }

  private emitCompleted(): void {
    if (this.completedEmitted) {
      return;
    }
    this.completedEmitted = true;
    this.activeIndex = -1;
    this.phase = 'completed';
    this.clearTimer();
    this.completed.emit();
  }

  private randomDuration(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  private handleReady(): void {
    this.readyReceived = true;
    this.phase = 'fast-forward';
    if (this.activeIndex === this.waitForReadyIndex && this.stepsState[this.activeIndex]?.state === 'active') {
      this.stepsState[this.activeIndex].state = 'done';
      this.runStep(this.activeIndex + 1);
      return;
    }
    if (this.activeIndex >= 0 && this.activeIndex < this.stepsState.length) {
      this.runStep(this.activeIndex);
    }
  }

  private shouldWaitForReady(index: number): boolean {
    return index === this.waitForReadyIndex && !this.readyReceived;
  }

  private shouldFastForwardStep(index: number): boolean {
    return this.readyReceived && this.phase === 'fast-forward' && index > this.waitForReadyIndex;
  }

  private clearTimer(): void {
    if (this.timerHandle !== null) {
      clearTimeout(this.timerHandle);
      this.timerHandle = null;
    }
  }
}
